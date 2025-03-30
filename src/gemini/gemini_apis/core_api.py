"""
gemini_apis/core_api.py - Core API functions for Gemini client

Provides low-level functions for interacting with the Gemini API:
- send_to_discord(response, prompt, is_final, source, content_type): Sends a Gemini response to Discord
- send_error_to_discord(error, prompt): Sends an error to Discord safely without risking recursion
- generate_content(prompt, temperature, system_instruction): Generates text based on a prompt
- generate_image(prompt, temperature): Generates an image based on a text prompt

Related files:
- src/gemini/gemini_client.py: Main client that orchestrates these API calls
- src/discord/discord_client.py: Client for Discord integration
"""

import os
import logging
from typing import Dict, Optional, Tuple, Union, Any
from io import BytesIO
from PIL import Image
from google.genai import types

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_to_discord(discord_client, response: str, prompt: str = None, is_final: bool = False,
                    source: str = None, content_type: str = "text") -> bool:
    """
    Send a Gemini response to Discord.

    Args:
        discord_client: Discord client instance to use for sending messages
        response: The response from Gemini
        prompt: The prompt that was sent to Gemini
        is_final: Whether this is the final response
        source: Source information (e.g., file being analyzed)
        content_type: Type of content being processed (text, image, audio, etc.)

    Returns:
        bool: True if successfully sent, False otherwise
    """
    try:
        # Format message with prompt if available
        message = response
        if prompt:
            message = f"**Prompt:**\n```\n{prompt}\n```\n\n**Response:**\n{response}"

        # Add content type as a header
        header = f"**{content_type.capitalize()}**\n"
        if source:
            header += f"**Source:** `{source}`\n"

        message = header + message

        # Send to appropriate Discord webhook based on type
        username = f"Gemini {content_type.capitalize()}"

        if is_final:
            # Send to analysis webhook
            success = discord_client.send_analysis_results(
                analysis=message,
                source=source,
                username=username
            )
        else:
            # Send to materials webhook
            success = discord_client.send_to_webhook(
                webhook_url=discord_client.webhook_ai_materials,
                content=message,
                username=username
            )

        if success:
            logger.info(f"Sent Gemini response to Discord ({content_type})")
        else:
            logger.warning(
                f"Failed to send Gemini response to Discord ({content_type})")

        return success

    except Exception as e:
        # Just log the error without trying to send it to Discord
        logger.error(f"Error preparing message for Discord: {str(e)}")
        # Don't try to send this error to Discord to avoid recursion
        return False


def send_error_to_discord(discord_client, error: Exception, prompt: str = None) -> bool:
    """
    Send an error to Discord safely without risking recursion.

    Args:
        discord_client: Discord client instance to use for sending errors
        error: The error that occurred
        prompt: The prompt that caused the error

    Returns:
        bool: True if successfully sent, False otherwise
    """
    try:
        # Create context dictionary if prompt is provided
        context = {"prompt": prompt} if prompt else None

        # Use the DiscordClient's send_error method
        success = discord_client.send_error(
            error=error,
            context=context
        )

        if success:
            logger.info("Error sent to Discord webhook")
        else:
            logger.warning("Failed to send error to Discord")

        return success

    except Exception as e:
        # If this fails, just log it and don't try to send it to Discord
        logger.error(f"Failed to send error to Discord: {str(e)}")
        return False


def generate_content(client, model_name: str, prompt: str, temperature: float = 0.7,
                     system_instruction: Optional[str] = None,
                     max_output_tokens: int = 8192,
                     top_p: float = 0.95,
                     top_k: int = 40) -> str:
    """
    Generate text based on a prompt using the Gemini API.

    Args:
        client: Initialized Gemini client instance
        model_name: The Gemini model to use
        prompt: Text prompt to generate content from
        temperature: Controls randomness (0.0-2.0)
        system_instruction: Optional instruction to guide the model's behavior
        max_output_tokens: Maximum number of tokens in the response
        top_p: Top-p sampling parameter
        top_k: Top-k sampling parameter

    Returns:
        str: Generated text
    """
    # Use the modern client API with system instruction
    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        top_p=top_p,
        top_k=top_k
    )

    if system_instruction:
        config.system_instruction = system_instruction

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=config
    )

    return response.text


def generate_image(client, prompt: str, temperature: float = 0.9) -> Tuple[Optional[str], Optional[Image.Image]]:
    """
    Generate an image based on a text prompt using Gemini's experimental model.

    Args:
        client: Initialized Gemini client instance
        prompt: Text description of the image to generate
        temperature: Controls randomness (0.0-2.0)

    Returns:
        Tuple of (response_text, image): The description text and generated image
    """
    logger.info("Attempting image generation with experimental model")

    # Try the experimental image generation model
    config = types.GenerateContentConfig(
        temperature=temperature,
        response_modalities=["Text", "Image"]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=prompt,
        config=config
    )

    description_text = None
    generated_image = None

    # Extract text and image from response
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            description_text = part.text
        elif hasattr(part, "inline_data") and part.inline_data:
            generated_image = Image.open(
                BytesIO(part.inline_data.data))

    if generated_image:
        logger.info("Successfully generated image with experimental model")
    else:
        logger.info("No image in response from experimental model")

    return description_text, generated_image
