"""
gemini_hooks/image_processor.py - Image processing workflows for Gemini

Provides high-level functions for image processing workflows:
- ImageProcessor: A class that handles the image processing pipeline
  - generate_image(prompt_data, output_filename): Generates an image from a prompt
  - save_prompt(prompt_data, filename): Saves a prompt to a JSON file
  
Related files:
- src/gemini/gemini_client.py: Main client that uses this processor
- src/gemini/gemini_apis/image_api.py: Lower-level image API functions
- src/gemini/gemini_utilities/file_utils.py: File utilities for saving images
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union, Tuple
from PIL import Image

from src.gemini.gemini_utilities.file_utils import save_json, save_image, ensure_directory
from src.gemini.gemini_apis.image_api import create_fallback_image

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageProcessor:
    """Handles image processing workflows for the Gemini client"""

    def __init__(self, client, output_dir: str = "output"):
        """
        Initialize the image processor with client and output directories

        Args:
            client: Gemini client instance
            output_dir: Base directory for all outputs
        """
        self.client = client
        self.output_dir = Path(output_dir)
        self.image_dir = self.output_dir / "images"
        self.prompt_dir = self.output_dir / "images/prompts"

        # Ensure directories exist
        ensure_directory(self.image_dir)
        ensure_directory(self.prompt_dir)

        logger.info("ImageProcessor initialized")

    def save_prompt(self, prompt_data: Dict[str, Any], filename: str) -> Path:
        """
        Save a prompt to a JSON file

        Args:
            prompt_data: Dictionary with prompt data
            filename: Base filename without extension

        Returns:
            Path: Path to the saved prompt file
        """
        prompt_path = self.prompt_dir / f"{filename}_prompt.json"
        save_json(prompt_data, prompt_path)
        return prompt_path

    def generate_image(self, prompt_data: Dict[str, Any], output_filename: str) -> Tuple[Optional[str], Optional[Path]]:
        """
        Generate an image based on a prompt and save it

        Args:
            prompt_data: Dictionary with prompt data
            output_filename: Base filename without extension

        Returns:
            Tuple of (description, image_path)
        """
        logger.info(f"Generating image for prompt: {output_filename}")

        # Extract the prompt text
        prompt_text = prompt_data.get("prompt", "")
        if not prompt_text:
            logger.error("Prompt text is empty")
            return None, None

        # Enhance the prompt with style information if available
        if "style" in prompt_data and "colors" in prompt_data:
            # Use up to 3 colors
            colors = prompt_data["colors"]
            if isinstance(colors, list):
                colors_str = ", ".join(colors[:3])
            else:
                colors_str = str(colors)

            enhanced_prompt = f"{prompt_text}. Art style: {prompt_data['style']}. Color palette: {colors_str}."
        else:
            enhanced_prompt = prompt_text

        try:
            # Generate the image
            config = {
                "temperature": 0.9,
                "response_modalities": ["Text", "Image"]
            }

            # Use the client's generate_image method instead of accessing models directly
            description_text, generated_image = self.client.generate_image(
                prompt=enhanced_prompt,
                temperature=0.9
            )

            if generated_image:
                # Save the image
                image_path = self.image_dir / f"{output_filename}_image.png"
                save_image(generated_image, image_path)
                logger.info(f"Image saved to {image_path}")
                return description_text, image_path
            else:
                logger.warning(f"No image generated for {output_filename}")
                # Create a fallback image
                fallback = create_fallback_image(
                    error_message="No image generated", color=(100, 149, 237))
                image_path = self.image_dir / f"{output_filename}_image.png"
                save_image(fallback, image_path)
                return description_text, image_path

        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            # Create fallback image
            fallback = create_fallback_image(
                error_message=str(e), color=(255, 0, 0))
            image_path = self.image_dir / f"{output_filename}_image.png"
            save_image(fallback, image_path)
            return f"Error: {str(e)}", image_path
