"""
discord_client.py - Discord Webhook Client

A client for sending messages to Discord webhooks with support for:
- Sending messages to Discord webhooks with chunking for long messages
- Support for Gemini AI operations (analysis, materials, errors)

Dependencies:
- requests
- logging
- json
- time

Related files: src/gemini/gemini_client.py
"""

import os
import json
import logging
import time
import requests
from typing import Dict, Any, Optional, Union, List
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)


class DiscordClient:
    """Client for sending messages to Discord webhooks"""

    def __init__(self):
        """
        Initialize the Discord client by loading webhook URLs from environment variables.
        """
        # Load environment variables
        load_dotenv()

        # Get webhook URLs from environment variables
        self.webhook_errors = os.environ.get("DISCORD_URL_WEBHOOK_ERRORS")
        self.webhook_ai_analysis = os.environ.get(
            "DISCORD_URL_WEBHOOK_AI_ANALYSIS")
        self.webhook_ai_materials = os.environ.get(
            "DISCORD_URL_WEBHOOK_AI_MATERIALS")

        # Default character limit per message
        self.char_limit = int(os.environ.get(
            "DISCORD_CHARACTER_PER_MESSAGE_LIMIT", 1950))

        # Validate webhook URLs
        if not self.webhook_errors:
            logger.warning(
                "Error webhook URL not found in environment variables")
        if not self.webhook_ai_analysis:
            logger.warning(
                "AI analysis webhook URL not found in environment variables")
        if not self.webhook_ai_materials:
            logger.warning(
                "AI materials webhook URL not found in environment variables")

    def send_to_webhook(self, webhook_url: str, content: str, username: str = None,
                        embed: Dict[str, Any] = None) -> bool:
        """
        Send a message to a Discord webhook. For longer messages, this
        automatically uses the send_long_message method for chunking.

        Args:
            webhook_url: The URL of the Discord webhook
            content: The message content to send
            username: Optional custom username for the webhook
            embed: Optional embed object to send with the message

        Returns:
            True if the message was sent successfully, False otherwise
        """
        if not webhook_url:
            logger.error("Cannot send to webhook: URL is missing")
            return False

        # For longer content, use the chunking method
        if content and len(content) > self.char_limit:
            return self.send_to_discord_webhook(webhook_url, content, username)

        # Prepare the payload
        payload = {}
        if content:
            payload["content"] = content
        if username:
            payload["username"] = username
        if embed:
            payload["embeds"] = [embed]

        # Send the request
        try:
            response = requests.post(
                webhook_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.status_code == 204 or (response.status_code >= 200 and response.status_code < 300)
        except Exception as e:
            logger.error(f"Failed to send message to webhook: {str(e)}")
            return False

    def send_to_discord_webhook(self, webhook_url: str, content: str, username: str = "Discord Bot", max_chars: int = 1950) -> bool:
        """
        Send a message to Discord, breaking it into chunks if needed.

        Args:
            webhook_url: Discord webhook URL
            content: Content to send
            username: Username to display in Discord
            max_chars: Maximum characters per message

        Returns:
            True if successful, False otherwise
        """
        try:
            # If the message is short enough, send it directly
            if len(content) <= max_chars:
                payload = {
                    "content": content,
                    "username": username
                }

                response = requests.post(
                    webhook_url,
                    data=json.dumps(payload),
                    headers={"Content-Type": "application/json"}
                )

                return response.status_code == 204

            # Otherwise, break it into chunks
            chunks = []
            current_chunk = ""

            # Split on line breaks to keep paragraphs together when possible
            lines = content.split('\n')

            for line in lines:
                # If adding this line would exceed the limit, start a new chunk
                if len(current_chunk) + len(line) + 1 > max_chars:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = line
                else:
                    if current_chunk:
                        current_chunk += '\n' + line
                    else:
                        current_chunk = line

            # Add the last chunk if it's not empty
            if current_chunk:
                chunks.append(current_chunk)

            # Send each chunk as a separate message
            success = True
            for i, chunk in enumerate(chunks):
                # Add part number for multi-part messages
                part_header = f"**Part {i+1}/{len(chunks)}**\n\n" if len(
                    chunks) > 1 else ""

                payload = {
                    "content": part_header + chunk,
                    "username": username
                }

                response = requests.post(
                    webhook_url,
                    data=json.dumps(payload),
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code != 204:
                    success = False
                    logger.warning(
                        f"Failed to send chunk {i+1}/{len(chunks)} to Discord: {response.status_code}")

                # Add a small delay between chunks to avoid rate limiting
                if i < len(chunks) - 1:
                    time.sleep(1)

            return success
        except Exception as e:
            logger.error(f"Error sending to Discord: {str(e)}")
            return False

    def send_error(self, error: Union[str, Exception], context: Dict[str, Any] = None) -> bool:
        """
        Send an error message to the errors webhook.

        Args:
            error: The error message or exception to send
            context: Optional context information about when the error occurred

        Returns:
            True if the message was sent successfully, False otherwise
        """
        if not self.webhook_errors:
            logger.warning("Error webhook URL not configured")
            return False

        # Format error message
        if isinstance(error, Exception):
            error_message = f"**Error:** `{type(error).__name__}: {str(error)}`"
        else:
            error_message = f"**Error:** `{error}`"

        # Add context if provided
        context_message = ""
        if context:
            context_message = "\n\n**Context:**\n```json\n" + \
                json.dumps(context, indent=2) + "\n```"

        # Combine message parts
        full_message = error_message + context_message

        # Send to webhook
        success = self.send_to_webhook(
            self.webhook_errors,
            full_message,
            username="Error Reporter"
        )

        # Log the error
        if success:
            logger.info(f"Error sent to Discord: {str(error)}")
        else:
            logger.error(f"Failed to send error to Discord: {str(error)}")

        return success

    def send_analysis_results(self, analysis: str, source: str = None, username: str = "AI Analysis") -> bool:
        """
        Send AI analysis results to the analysis webhook.

        Args:
            analysis: The analysis text to send
            source: Optional source information (e.g., file being analyzed)
            username: Username to display in Discord

        Returns:
            True if the message was sent successfully, False otherwise
        """
        if not self.webhook_ai_analysis:
            logger.warning("Analysis webhook URL not configured")
            return False

        # Format message with source if provided
        message = analysis
        if source:
            message = f"**Source:** `{source}`\n\n{analysis}"

        # Send to webhook
        return self.send_to_discord_webhook(
            self.webhook_ai_analysis,
            message,
            username=username
        )

    def send_summary(self, title: str, summary: str, details: Optional[List[Dict[str, Any]]] = None, username: str = "Gemini Pipeline") -> bool:
        """
        Send a summary message to the materials webhook.

        Args:
            title: The title of the summary
            summary: The summary text
            details: Optional list of details to include
            username: Username to display in Discord

        Returns:
            True if the message was sent successfully, False otherwise
        """
        if not self.webhook_ai_materials:
            logger.warning("Materials webhook URL not configured")
            return False

        # Format the message
        message = f"**{title}**\n\n{summary}"

        # Add details if provided
        if details:
            message += "\n\n**Details:**"
            for i, detail in enumerate(details):
                status = "✅ Success" if detail.get(
                    "success", False) else "❌ Failed"
                error_info = f" - Error: {detail.get('error', 'Unknown error')}" if not detail.get(
                    "success", False) else ""
                message += f"\n{i+1}. {detail.get('name', f'Item {i+1}')} - {
                    status}{error_info}"

        # Send to webhook
        return self.send_to_discord_webhook(
            self.webhook_ai_materials,
            message,
            username=username
        )


# Example usage
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Create client
    discord_client = DiscordClient()

    # Example: Send a test message to webhook
    discord_client.send_to_discord_webhook(
        discord_client.webhook_ai_materials or "https://discord.com/api/webhooks/your-webhook-url",
        "This is a test message from the Discord client.\n\nIt demonstrates the chunking capability for long messages.",
        username="Discord Test Bot"
    )
