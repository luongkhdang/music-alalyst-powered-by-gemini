"""
analyzer_api.py - Gemini API interface for content analysis

Provides interfaces for:
- Image analysis
- Audio file analysis 
- Multimodal content analysis

Dependencies:
- google.generativeai
- PIL
- dotenv

Related files:
- src/gemini/gemini_utilities/rate_limiter.py
- src/gemini/gemini_client.py
"""

import os
import logging
from typing import List, Dict, Any, Optional, Union
from io import BytesIO
from PIL import Image
import google.generativeai as genai
# Import the modern Google AI client API
from google import genai as modern_genai
from google.genai import types
from ..gemini_utilities.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)


class AnalyzerAPI:
    """API interface for Gemini content analysis capabilities"""

    def __init__(self, api_key: str, model_name: str, rate_limiter: RateLimiter, client=None):
        """
        Initialize the analyzer API.

        Args:
            api_key: Gemini API key
            model_name: The model to use for analysis
            rate_limiter: Rate limiter instance to control API usage
            client: Optional modern client instance
        """
        self.api_key = api_key
        self.model_name = model_name
        self.rate_limiter = rate_limiter

        # Use the provided client or initialize a new one
        self.client = client or modern_genai.Client(api_key=api_key)

        # Set flag for checking client availability
        self.has_modern_client = client is not None

    def analyze_image(self,
                      image_path_or_object: Union[str, Image.Image],
                      prompt: str,
                      temperature: float = 0.2) -> str:
        """
        Analyze an image with a text prompt.

        Args:
            image_path_or_object: Path to the image file or PIL Image object
            prompt: Text prompt describing what to analyze about the image
            temperature: Controls randomness (0.0-2.0)

        Returns:
            Analysis text
        """
        # Apply rate limiting
        self.rate_limiter.check_and_wait()

        # Handle both file paths and Image objects
        if isinstance(image_path_or_object, str):
            image = Image.open(image_path_or_object)
        else:
            image = image_path_or_object

        # Use the modern client API
        try:
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=8100
            )

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt, image],
                config=config
            )

            return response.text
        except Exception as e:
            logger.warning(f"Modern API failed for image analysis: {e}")

            # Fall back to legacy implementation
            model = genai.GenerativeModel(model_name=self.model_name)
            response = model.generate_content(
                contents=[image, prompt],
                generation_config={"temperature": temperature}
            )

            return response.text

    def analyze_audio(self, audio_path_or_file: Union[str, Any], prompt: str) -> str:
        """
        Analyze an audio file (like MP3) with a text prompt.

        Args:
            audio_path_or_file: Path to the audio file or uploaded file reference
            prompt: Text prompt describing what to analyze about the audio

        Returns:
            Analysis text
        """
        # Apply rate limiting
        self.rate_limiter.check_and_wait()

        try:
            # If given a path, upload the file using the modern API
            if isinstance(audio_path_or_file, str):
                audio_file = self.client.files.upload(file=audio_path_or_file)

                config = types.GenerateContentConfig(
                    temperature=0.4,
                    max_output_tokens=8100
                )

                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[prompt, audio_file],
                    config=config
                )

                return response.text
            else:
                # For non-string objects, try using them directly
                config = types.GenerateContentConfig(
                    temperature=0.4,
                    max_output_tokens=8100
                )

                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[prompt, audio_path_or_file],
                    config=config
                )

                return response.text

        except Exception as e:
            logger.warning(f"Modern API failed for audio analysis: {e}")

            # Fall back to legacy implementation using old API
            if isinstance(audio_path_or_file, str):
                audio_file = genai.upload_file(path=audio_path_or_file)
            else:
                audio_file = audio_path_or_file

            # Use the GenerativeModel to analyze the audio file
            model = genai.GenerativeModel(model_name=self.model_name)
            response = model.generate_content(
                contents=[prompt, audio_file]
            )

            return response.text

    def analyze_multimodal(self,
                           contents: List[Union[str, Dict, Image.Image, Any]],
                           temperature: float = 0.4) -> str:
        """
        Analyze multiple types of content (text, images, audio) in a single request.

        Args:
            contents: List of content items (text strings, images, file references)
            temperature: Controls randomness (0.0-2.0)

        Returns:
            Analysis text
        """
        # Apply rate limiting
        self.rate_limiter.check_and_wait()

        try:
            # Use the modern client API
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=8100
            )

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config
            )

            return response.text
        except Exception as e:
            logger.warning(f"Modern API failed for multimodal analysis: {e}")

            # Fall back to legacy implementation
            try:
                # Create a model instance for multimodal analysis
                model = genai.GenerativeModel(
                    self.model_name,
                    generation_config={
                        "temperature": temperature,
                        "max_output_tokens": 8100
                    }
                )

                # Generate response with multimodal content
                response = model.generate_content(contents)

                # Return the text response
                return response.text

            except Exception as inner_e:
                logger.error(f"Error in multimodal analysis: {str(inner_e)}")
                raise

    def upload_file(self, file_path: str) -> Any:
        """
        Upload a file to be used with Gemini. Supports MP3, images, and other file types.

        Args:
            file_path: Path to the file to upload

        Returns:
            File object reference
        """
        # Apply rate limiting - file uploads count against the API rate
        self.rate_limiter.check_and_wait()

        try:
            # Use the modern client API
            return self.client.files.upload(file=file_path)
        except Exception as e:
            logger.warning(f"Modern API file upload failed: {e}")

            # Fall back to legacy implementation
            return genai.upload_file(path=file_path)
