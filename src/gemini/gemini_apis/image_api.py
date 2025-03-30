"""
gemini_apis/image_api.py - Image processing and analysis API for Gemini

Provides functions for processing, analyzing and generating images:
- analyze_image(client, image_path_or_file, prompt, temperature): Analyzes images with Gemini
- create_fallback_image(error_message, color): Creates a simple colored fallback image 
- process_generated_image(response): Extracts image and description from Gemini response

Related files:
- src/gemini/gemini_client.py: Main client that uses these API functions
- src/gemini/gemini_apis/core_api.py: Core API functions used by this module
"""

import logging
from typing import Union, Optional, Tuple, Dict, Any
from io import BytesIO
from pathlib import Path
from PIL import Image
from google.genai import types

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_image(client, image_path_or_file: Union[str, Image.Image, Path],
                  prompt: str,
                  temperature: float = 0.4) -> str:
    """
    Analyze an image with a prompt for guidance.

    Args:
        client: Initialized Gemini client instance
        image_path_or_file: Path to image file, Path object, or PIL Image object
        prompt: Text prompt to guide the analysis
        temperature: Controls randomness (0.0-2.0)

    Returns:
        str: Analysis text from Gemini
    """
    # Prepare the image
    if isinstance(image_path_or_file, Path):
        image_path_or_file = str(image_path_or_file)

    if isinstance(image_path_or_file, str):
        image = Image.open(image_path_or_file)
    else:
        image = image_path_or_file

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=8192
    )

    response = client.models.generate_content(
        model=client.model_name,
        contents=[prompt, image],
        config=config
    )

    return response.text


def create_fallback_image(error_message: str = None, color: tuple = (255, 0, 0)) -> Image.Image:
    """
    Create a simple colored image as a fallback when image generation fails.

    Args:
        error_message: Optional error message (not used in the image, just for logging)
        color: RGB color tuple for the image (default is red for errors)

    Returns:
        PIL.Image: A simple colored image
    """
    if error_message:
        logger.warning(
            f"Creating fallback image due to error: {error_message}")

    # Create a simple colored image as a fallback (512x512 px)
    fallback_image = Image.new('RGB', (512, 512), color)
    return fallback_image


def process_generated_image(response) -> Tuple[Optional[str], Optional[Image.Image]]:
    """
    Extract text description and image from a Gemini image generation response.

    Args:
        response: Response from Gemini image generation API

    Returns:
        Tuple of (description_text, generated_image)
    """
    description_text = None
    generated_image = None

    # Extract text and image from response
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            description_text = part.text
        elif hasattr(part, "inline_data") and part.inline_data:
            generated_image = Image.open(
                BytesIO(part.inline_data.data))

    return description_text, generated_image
