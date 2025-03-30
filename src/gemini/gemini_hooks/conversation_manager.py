"""
conversation_manager.py - Conversation management for Gemini API

Provides functionality for:
- Creating and managing chat sessions with Gemini API
- Sending messages in a conversation context
- Retrieving conversation history

Dependencies:
- google.generativeai
- PIL
- typing

Related files:
- src/gemini/gemini_utilities/rate_limiter.py
- src/gemini/gemini_client.py
"""

import logging
from typing import List, Dict, Any, Optional, Union, Generator
from PIL import Image
import google.generativeai as genai
from ..gemini_utilities.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)


class ConversationManager:
    """Manages conversations/chat sessions with Gemini API"""

    def __init__(self, api_key: str, model_name: str, rate_limiter: RateLimiter):
        """
        Initialize the conversation manager.

        Args:
            api_key: Gemini API key
            model_name: The model to use for the conversation
            rate_limiter: Rate limiter instance to control API usage
        """
        self.api_key = api_key
        self.model_name = model_name
        self.rate_limiter = rate_limiter
        self.current_chat = None

    def create_chat(self, system_instruction: Optional[str] = None) -> None:
        """
        Create a new chat session.

        Args:
            system_instruction: Optional system instruction to guide model behavior
        """
        # Create chat doesn't count against rate limit

        # Get the generative model
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_instruction
        )

        # Start a new chat session
        self.current_chat = model.start_chat(history=[])

    def send_message(self,
                     message: Union[str, List[Union[str, Dict, Image.Image]]],
                     temperature: float = 0.7) -> str:
        """
        Send a message in the current chat session. Supports multimodal inputs.

        Args:
            message: The message to send - can be text, image, or a list of content items
            temperature: Controls randomness (0.0-2.0)

        Returns:
            Response text
        """
        # Apply rate limiting
        self.rate_limiter.check_and_wait()

        if not self.current_chat:
            self.create_chat()

        # Send the message to the chat
        response = self.current_chat.send_message(
            message,
            generation_config={"temperature": temperature}
        )

        return response.text

    def stream_message(self,
                       message: Union[str, List[Union[str, Dict, Image.Image]]],
                       temperature: float = 0.7) -> Generator:
        """
        Stream a message in the current chat session. Supports multimodal inputs.

        Args:
            message: The message to send - can be text, image, or a list of content items
            temperature: Controls randomness (0.0-2.0)

        Returns:
            Generator yielding response chunks
        """
        # Apply rate limiting
        self.rate_limiter.check_and_wait()

        if not self.current_chat:
            self.create_chat()

        # Send the message to the chat with streaming
        response = self.current_chat.send_message(
            message,
            generation_config={"temperature": temperature},
            stream=True
        )

        for chunk in response:
            if chunk.text:
                yield chunk.text

    def get_chat_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of the current chat session.

        Returns:
            List of messages in the chat history
        """
        # Get history doesn't count against rate limit

        if not self.current_chat:
            return []

        history = []
        for message in self.current_chat.history:
            role = "user" if message.role == "user" else "model"

            # Extract content which might be text or binary data
            content = None
            if hasattr(message, "parts"):
                for part in message.parts:
                    if hasattr(part, "text") and part.text:
                        content = part.text
                        break
                    elif hasattr(part, "inline_data") and part.inline_data:
                        content = {
                            "mime_type": part.inline_data.mime_type,
                            "data_type": "binary_data"
                        }
                        break

            history.append({
                "role": role,
                "content": content
            })

        return history
