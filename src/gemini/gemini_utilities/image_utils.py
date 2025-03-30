"""
image_utils.py - Image handling utilities for Gemini client

Provides utilities for:
- Creating fallback/placeholder images when API calls fail
- Image processing functionality for use with Gemini API

Dependencies:
- PIL (Pillow)
- io
"""

import logging
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from typing import Optional

logger = logging.getLogger(__name__)


def create_fallback_image(error_message: Optional[str], prompt: str) -> Image.Image:
    """
    Create a placeholder image when image generation fails or as a visualization.

    Args:
        error_message: The error message to display (None if no error)
        prompt: The original prompt or description text

    Returns:
        PIL Image object with error information or description visualization
    """
    # Create a standard sized image
    width, height = 512, 512

    # If there's no error, create a visualization of the description
    if error_message is None:
        # Generate a gradient background based on the text content
        image = _create_description_visualization(prompt, width, height)
        return image

    # Otherwise create an error image
    image = Image.new('RGB', (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(image)

    # Add title
    draw.text((20, 30), "Image Generation Failed", fill=(200, 0, 0))
    draw.text(
        (20, 50), prompt[:50] + "..." if len(prompt) > 50 else prompt, fill=(0, 0, 200))

    # Add separator line
    draw.line([(20, 80), (width-20, 80)],
              fill=(200, 200, 200), width=2)

    # Add error message
    error_msg = str(error_message)
    lines = []
    line = ""
    for word in error_msg.split():
        if len(line + " " + word) <= 40:  # 40 chars per line
            line = line + " " + word if line else word
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)

    y_position = 100
    for line in lines[:10]:
        draw.text((20, y_position), line, fill=(200, 0, 0))
        y_position += 25

    # Add note about fallback
    draw.text((20, height-50),
              "Note: This is a fallback placeholder image.", fill=(0, 0, 0))
    draw.text((20, height-30),
              "The actual image generation API call failed.", fill=(0, 0, 0))

    logger.info("Falling back to placeholder image generation")
    return image


def _create_description_visualization(description: str, width: int, height: int) -> Image.Image:
    """
    Create a simple visualization based on a text description.

    Args:
        description: The text description to visualize
        width: Image width
        height: Image height

    Returns:
        A PIL Image representing the description
    """
    # Generate a color palette based on the text
    def text_to_color(text):
        # Simple hash-based approach to get consistent colors from text
        hash_val = sum(ord(c) for c in text)
        r = (hash_val * 1234) % 256
        g = (hash_val * 2345) % 256
        b = (hash_val * 3456) % 256
        return (r, g, b)

    # Get base colors from the description
    base_color = text_to_color(
        description[:20]) if description else (100, 100, 200)
    accent_color = ((base_color[0] + 128) % 256,
                    (base_color[1] + 128) % 256,
                    (base_color[2] + 128) % 256)

    # Create gradient background
    image = Image.new('RGB', (width, height), color=base_color)
    draw = ImageDraw.Draw(image)

    # Add some random shapes based on the description
    for i in range(10):
        # Use different parts of the description for different shapes
        shape_seed = description[i*5:(i+1)*5] if i * \
            5 < len(description) else str(i)
        shape_color = text_to_color(shape_seed)

        # Draw either circle, rectangle, or line
        shape_type = sum(ord(c) for c in shape_seed) % 3
        x1 = (sum(ord(c) for c in shape_seed) * 1234) % width
        y1 = (sum(ord(c) for c in shape_seed) * 2345) % height
        size = (sum(ord(c) for c in shape_seed) * 3456) % 100 + 20

        if shape_type == 0:  # Circle
            draw.ellipse([x1, y1, x1+size, y1+size], fill=shape_color)
        elif shape_type == 1:  # Rectangle
            draw.rectangle([x1, y1, x1+size, y1+size], fill=shape_color)
        else:  # Line
            x2 = (x1 + size*2) % width
            y2 = (y1 + size*2) % height
            draw.line([x1, y1, x2, y2], fill=shape_color, width=5)

    # Add text with description summary
    summary = description[:100] + \
        "..." if len(description) > 100 else description
    # Draw a background box for text
    text_box_height = 80
    draw.rectangle([0, height-text_box_height, width, height],
                   fill=(255, 255, 255, 180))

    # Add the text in chunks
    lines = []
    line = ""
    for word in summary.split():
        if len(line + " " + word) <= 40:  # 40 chars per line
            line = line + " " + word if line else word
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)

    # Draw the text
    y_position = height - text_box_height + 10
    for line in lines[:3]:
        draw.text((10, y_position), line, fill=(0, 0, 0))
        y_position += 20

    # Add a border
    for i in range(3):
        draw.rectangle([i, i, width-i-1, height-i-1], outline=accent_color)

    logger.info("Created visualization from description text")
    return image
