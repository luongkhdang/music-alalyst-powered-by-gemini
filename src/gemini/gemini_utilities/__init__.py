"""
gemini_utilities/__init__.py - Utility package for Gemini client

Exports utility functions to support the Gemini client:
- File utilities: For file operations
- Rate limiter: For API rate limiting
- Image utilities: For image processing

Related files:
- src/gemini/gemini_client.py: Main client that uses these utilities
"""

from src.gemini.gemini_utilities.file_utils import (
    save_text,
    save_json,
    save_image,
    ensure_directory,
    clean_output_directory
)

from src.gemini.gemini_utilities.image_utils import (
    create_fallback_image,
    _create_description_visualization
)

from src.gemini.gemini_utilities.rate_limiter import (
    RateLimiter
)

__all__ = [
    # File utilities
    'save_text',
    'save_json',
    'save_image',
    'ensure_directory',
    'clean_output_directory',

    # Image utilities
    'create_fallback_image',
    '_create_description_visualization',

    # Rate limiting
    'RateLimiter'
]
