"""
generator_api.py - Gemini API interface for content generation

Provides interfaces for:
- Text generation
- Image generation
- Multimodal content generation

Dependencies:
- google.generativeai
- PIL
- io
- dotenv

Related files:
- src/gemini/gemini_utilities/image_utils.py
- src/gemini/gemini_utilities/rate_limiter.py
- src/gemini/gemini_client.py
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Union, Generator, Tuple
from io import BytesIO
from PIL import Image
import google.generativeai as genai
# Import the modern Google AI client API
from google import genai as modern_genai
from google.genai import types
from ..gemini_utilities.rate_limiter import RateLimiter
from ..gemini_utilities.image_utils import create_fallback_image

logger = logging.getLogger(__name__)


class GeneratorAPI:
    """API interface for Gemini content generation capabilities"""

    def __init__(self, api_key: str, model_name: str, rate_limiter: RateLimiter, client=None):
        """
        Initialize the generator API.

        Args:
            api_key: Gemini API key
            model_name: The model to use for generation
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

    def generate_content(self,
                         prompt: Union[str, List[Union[str, Dict, Image.Image]]],
                         system_instruction: Optional[str] = None,
                         temperature: float = 0.7,
                         max_output_tokens: int = 4096,
                         top_p: float = 0.95,
                         top_k: int = 40,
                         stop_sequences: Optional[List[str]] = None) -> str:
        """
        Generate content using the Gemini model with support for multimodal inputs.

        Args:
            prompt: The text prompt or list of content items to send to the model
                Can include text strings, images, or file references
            system_instruction: Optional system instruction to guide model behavior
            temperature: Controls randomness (0.0-2.0)
            max_output_tokens: Maximum number of tokens in response
            top_p: Token filtering by cumulative probability
            top_k: Limits token selection to k most probable options
            stop_sequences: List of sequences that halt generation

        Returns:
            Generated text response
        """
        # Apply rate limiting
        self.rate_limiter.check_and_wait()

        # Use the modern client API
        try:
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                top_p=top_p,
                top_k=top_k
            )

            if system_instruction:
                config.system_instruction = system_instruction

            if stop_sequences:
                config.stop_sequences = stop_sequences

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            return response.text
        except Exception as e:
            logger.warning(f"Modern API failed for content generation: {e}")

            # Fall back to legacy implementation
            # If system instruction is provided but using the legacy API, prepend it to the prompt
            if system_instruction and isinstance(prompt, str):
                enhanced_prompt = f"SYSTEM: {system_instruction}\n\nUSER: {prompt}"
                prompt = enhanced_prompt

            # Get the generative model
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction if not isinstance(
                    prompt, str) else None
            )

            # Set the generation config
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
                "top_p": top_p,
                "top_k": top_k
            }

            if stop_sequences:
                generation_config["stop_sequences"] = stop_sequences

            # Generate content
            response = model.generate_content(
                contents=prompt,
                generation_config=generation_config
            )

            return response.text

    def stream_content(self,
                       prompt: Union[str, List[Union[str, Dict, Image.Image]]],
                       system_instruction: Optional[str] = None,
                       temperature: float = 0.7,
                       max_output_tokens: int = 4096,
                       top_p: float = 0.95,
                       top_k: int = 40,
                       stop_sequences: Optional[List[str]] = None) -> Generator:
        """
        Stream content generation from the Gemini model with support for multimodal inputs.

        Args:
            prompt: The text prompt or list of content items to send to the model
                Can include text strings, images, or file references
            system_instruction: Optional system instruction to guide model behavior
            temperature: Controls randomness (0.0-2.0)
            max_output_tokens: Maximum number of tokens in response
            top_p: Token filtering by cumulative probability
            top_k: Limits token selection to k most probable options
            stop_sequences: List of sequences that halt generation

        Returns:
            Generator yielding response chunks
        """
        # Apply rate limiting
        self.rate_limiter.check_and_wait()

        # Use the modern client API for streaming
        try:
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                top_p=top_p,
                top_k=top_k
            )

            if system_instruction:
                config.system_instruction = system_instruction

            if stop_sequences:
                config.stop_sequences = stop_sequences

            response_stream = self.client.models.generate_content_stream(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            for chunk in response_stream:
                if hasattr(chunk, "text") and chunk.text:
                    yield chunk.text

            return
        except Exception as e:
            logger.warning(f"Modern API streaming failed: {e}")

            # Fall back to legacy implementation
            # If system instruction is provided but using the legacy API, prepend it to the prompt
            if system_instruction and isinstance(prompt, str):
                enhanced_prompt = f"SYSTEM: {system_instruction}\n\nUSER: {prompt}"
                prompt = enhanced_prompt

            # Get the generative model
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction if not isinstance(
                    prompt, str) else None
            )

            # Set the generation config
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
                "top_p": top_p,
                "top_k": top_k
            }

            if stop_sequences:
                generation_config["stop_sequences"] = stop_sequences

            # Generate content in streaming mode
            response = model.generate_content(
                contents=prompt,
                generation_config=generation_config,
                stream=True
            )

            for chunk in response:
                if chunk.text:
                    yield chunk.text

    def generate_image(self, prompt: str, temperature: float = 0.9) -> Tuple[Optional[str], Optional[Image.Image]]:
        """
        Generate an image based on a text prompt using Gemini's image generation capability.

        Note: This uses the experimental image generation feature in Gemini API.
        For Gemini 2.0 models, image generation is actually done by generating text
        descriptions that can be used with external image generation services.

        Args:
            prompt: Text description of the image to generate
            temperature: Controls randomness (0.0-2.0)

        Returns:
            Tuple of (response_text, image)
        """
        # Apply rate limiting
        self.rate_limiter.check_and_wait()

        # Try using the modern client API with experimental image generation
        try:
            config = types.GenerateContentConfig(
                temperature=temperature,
                response_modalities=["Text", "Image"]
            )

            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp-image-generation",
                contents=prompt,
                config=config
            )

            description_text = None
            image = None

            # Extract text and image from response
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    description_text = part.text
                elif hasattr(part, "inline_data") and part.inline_data:
                    image = Image.open(BytesIO(part.inline_data.data))

            if image:
                logger.info(
                    "Successfully generated image with experimental model")
                return description_text, image

            # If we got a description but no image, create a visualization
            if description_text:
                logger.info(
                    "Got description but no image, creating visualization")
                fallback_image = create_fallback_image(None, description_text)
                return description_text, fallback_image

            # If we didn't get any useful response, fall back to text-only description
            raise ValueError("No useful response from image generation API")

        except Exception as e:
            logger.warning(f"Modern API for image generation failed: {e}")

            # Fall back to text-based description approach
            try:
                # Create a model instance for text-based image description
                config = types.GenerateContentConfig(
                    temperature=temperature,
                    response_mime_type="application/json",
                    max_output_tokens=500
                )

                # Enhanced prompt for image description
                enhanced_prompt = f"""
                Generate a detailed image description based on this prompt: "{prompt}"
                
                The description should include:
                1. The main subject or scene
                2. Specific visual details (colors, lighting, texture)
                3. Mood and atmosphere
                4. Style (realistic, abstract, etc.)
                
                Format your response as JSON with the following structure:
                {{
                    "description": "Detailed visual description",
                    "style": "Artistic style (realistic, abstract, anime, etc.)",
                    "colors": ["primary color", "secondary color", "accent color"],
                    "mood": "Overall mood or feeling"
                }}
                """

                # Generate content with text description
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=enhanced_prompt,
                    config=config
                )

                # Extract the JSON description
                try:
                    description_json = json.loads(response.text)
                    description_text = description_json.get("description", "")

                    # Create a fallback image with the description
                    image = create_fallback_image(None, description_text)

                    return response.text, image

                except json.JSONDecodeError:
                    # If response is not valid JSON, use the text as is
                    logger.warning(
                        "Image description response was not valid JSON")
                    image = create_fallback_image(None, response.text[:200])
                    return response.text, image

            except Exception as inner_e:
                logger.error(
                    f"Both image generation approaches failed: {str(inner_e)}")

                # Fall back to legacy implementation as a last resort
                try:
                    # Create a model instance for text-based image description
                    model = genai.GenerativeModel(
                        model_name=self.model_name)

                    # Enhanced prompt for image description
                    enhanced_prompt = f"""
                    Generate a detailed image description based on this prompt: "{prompt}"
                    
                    The description should include:
                    1. The main subject or scene
                    2. Specific visual details (colors, lighting, texture)
                    3. Mood and atmosphere
                    4. Style (realistic, abstract, etc.)
                    
                    Format your response as JSON with the following structure:
                    {{
                        "description": "Detailed visual description",
                        "style": "Artistic style (realistic, abstract, anime, etc.)",
                        "colors": ["primary color", "secondary color", "accent color"],
                        "mood": "Overall mood or feeling"
                    }}
                    """

                    # Set generation config
                    generation_config = {
                        "temperature": temperature,
                        "response_mime_type": "application/json",
                        "max_output_tokens": 500
                    }

                    # Generate content with text description
                    response = model.generate_content(
                        enhanced_prompt,
                        generation_config=generation_config
                    )

                    # Extract the JSON description
                    try:
                        description_json = json.loads(response.text)
                        description_text = description_json.get(
                            "description", "")

                        # Create a fallback image with the description
                        image = create_fallback_image(None, description_text)

                        return response.text, image

                    except json.JSONDecodeError:
                        # If response is not valid JSON, use the text as is
                        logger.warning(
                            "Image description response was not valid JSON")
                        image = create_fallback_image(
                            None, response.text[:200])
                        return response.text, image

                except Exception as e:
                    logger.error(f"Error generating image: {str(e)}")

                    # Create a fallback image with error information
                    image = create_fallback_image(e, prompt)

                    return f"Error generating image: {str(e)}", image
