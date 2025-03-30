"""
gemini/__init__.py - Gemini package for AI analysis and generation

Exports the main classes and processors:
- GeminiClient: Main client for interacting with Google's Gemini API
- AudioToImageProcessor: Process audio files into images
- AudioProcessor: Process audio files
- ImageProcessor: Process image generation

Related files:
- src/gemini/gemini_client.py: Main client implementation
- src/gemini/gemini_apis/: API functions
- src/gemini/gemini_hooks/: Workflow processors
- src/gemini/gemini_prompts/: Prompt templates
- src/gemini/gemini_utilities/: Utility functions
"""

from src.gemini.gemini_client import GeminiClient
from src.gemini.gemini_hooks import (
    AudioProcessor,
    ImageProcessor,
    AudioToImageProcessor,
    ConversationManager
)

__all__ = [
    'GeminiClient',
    'AudioProcessor',
    'ImageProcessor',
    'AudioToImageProcessor',
    'ConversationManager'
]
