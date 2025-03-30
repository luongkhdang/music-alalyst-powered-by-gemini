"""
gemini_apis/multimodal_api.py - Multimodal content analysis API for Gemini

Provides functions for analyzing multiple content types together:
- analyze_multimodal(client, contents, temperature): Analyzes multiple content types in a single request
- determine_content_type(item): Determines the type of content for logging purposes

Related files:
- src/gemini/gemini_client.py: Main client that uses these API functions
- src/gemini/gemini_apis/core_api.py: Core API functions used by this module
"""

import logging
from typing import List, Union, Dict, Any
from PIL import Image
from google.genai import types

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def determine_content_type(item: Any) -> str:
    """
    Determine the type of a content item for logging purposes.

    Args:
        item: Content item to check

    Returns:
        str: Simple description of content type
    """
    if isinstance(item, str):
        return "text"
    elif isinstance(item, Image.Image):
        return "image"
    elif hasattr(item, "mime_type"):
        if "audio" in item.mime_type:
            return "audio"
        elif "image" in item.mime_type:
            return "image"
        else:
            return f"file ({item.mime_type})"
    else:
        return "unknown"


def analyze_multimodal(client, contents: List[Union[str, Dict, Image.Image, Any]],
                       temperature: float = 0.4) -> str:
    """
    Analyze multiple types of content (text, images, audio) in a single request.

    Args:
        client: Initialized Gemini client instance
        contents: List of content items (text strings, images, file references)
        temperature: Controls randomness (0.0-2.0)

    Returns:
        str: Analysis text from Gemini
    """
    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=8192
    )

    response = client.models.generate_content(
        model=client.model_name,
        contents=contents,
        config=config
    )

    # Log the content types for debugging
    content_types = [determine_content_type(item) for item in contents]
    logger.info(
        f"Analyzed {len(contents)} multimodal items: {', '.join(content_types)}")

    return response.text
