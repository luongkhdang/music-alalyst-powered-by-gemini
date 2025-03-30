"""
gemini_apis/__init__.py - API package for Gemini client

Exports low-level API functions for direct interaction with Gemini:
- Core API: Text generation, error handling, Discord integration
- Audio API: Audio processing and analysis
- Image API: Image generation and analysis
- File API: File upload, listing, and deletion
- Chat API: Chat session management
- Multimodal API: Analyzing mixed content types

Related files:
- src/gemini/gemini_client.py: Main client that uses these APIs
"""

from src.gemini.gemini_apis.core_api import (
    send_to_discord,
    send_error_to_discord,
    generate_content,
    generate_image
)

from src.gemini.gemini_apis.audio_api import (
    analyze_audio,
    create_audio_analysis_prompt
)

from src.gemini.gemini_apis.image_api import (
    analyze_image,
    create_fallback_image,
    process_generated_image
)

from src.gemini.gemini_apis.chat_api import (
    create_chat,
    send_message,
    get_chat_history
)

from src.gemini.gemini_apis.multimodal_api import (
    analyze_multimodal,
    determine_content_type
)

from src.gemini.gemini_apis.file_api import (
    list_files,
    delete_file,
    upload_file
)

__all__ = [
    # Core API
    'send_to_discord',
    'send_error_to_discord',
    'generate_content',
    'generate_image',

    # Audio API
    'analyze_audio',
    'create_audio_analysis_prompt',

    # Image API
    'analyze_image',
    'create_fallback_image',
    'process_generated_image',

    # Chat API
    'create_chat',
    'send_message',
    'get_chat_history',

    # Multimodal API
    'analyze_multimodal',
    'determine_content_type',

    # File API
    'list_files',
    'delete_file',
    'upload_file'
]
