"""
gemini_apis/chat_api.py - Chat and conversation API for Gemini

Provides functions for managing chat sessions with Gemini:
- create_chat(client, model_name, system_instruction): Creates a new chat session
- send_message(chat, text, stream): Sends a message to an existing chat session
- get_chat_history(chat): Gets the conversation history from a chat session

Related files:
- src/gemini/gemini_client.py: Main client that uses these chat functions
- src/gemini/gemini_hooks/conversation_manager.py: Higher-level conversation management
"""

import logging
from typing import Optional, List, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_chat(client, model_name: str, system_instruction: Optional[str] = None):
    """
    Create a new chat session with an optional system instruction.

    Args:
        client: Gemini client instance
        model_name: Name of the model to use for the chat
        system_instruction: Optional instruction to guide the model's behavior

    Returns:
        The chat object
    """
    # Create a chat session using client API
    chat = client.chats.create(model=model_name)

    # Send system instruction as first message if provided
    if system_instruction:
        chat.send_message(f"System: {system_instruction}")

    return chat


def send_message(chat, text: str, stream: bool = False):
    """
    Send a message to the chat session.

    Args:
        chat: Chat session object
        text: The message text to send
        stream: Whether to stream the response

    Returns:
        Chat response or stream
    """
    # Send message to Gemini
    if stream:
        # Handle streaming response
        return chat.send_message_stream(text)
    else:
        # Handle regular response
        return chat.send_message(text)


def get_chat_history(chat) -> List[Any]:
    """
    Get the history of the current chat session.

    Args:
        chat: Chat session object

    Returns:
        List of chat messages
    """
    if chat is None:
        return []

    return chat.get_history()
