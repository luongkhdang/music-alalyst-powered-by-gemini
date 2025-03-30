"""
gemini_hooks/__init__.py - Hook package for Gemini client

Exports high-level workflow classes that coordinate API calls:
- AudioProcessor: Audio analysis and processing workflows
- ImageProcessor: Image generation and processing workflows
- ConversationManager: Chat and conversation management
- AudioToImageProcessor: Complete audio-to-image pipeline

Related files:
- src/gemini/gemini_client.py: Main client that uses these hooks
- src/gemini/gemini_apis/: Low-level API functions used by these hooks
"""

from src.gemini.gemini_hooks.audio_processor import AudioProcessor
from src.gemini.gemini_hooks.image_processor import ImageProcessor
from src.gemini.gemini_hooks.conversation_manager import ConversationManager
from src.gemini.gemini_hooks.audio_to_image_processor import AudioToImageProcessor

__all__ = [
    'AudioProcessor',
    'ImageProcessor',
    'ConversationManager',
    'AudioToImageProcessor'
]
