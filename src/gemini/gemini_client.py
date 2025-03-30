"""
gemini_client.py - Unified Gemini Client

An advanced AI client capable of processing images, MP3 files, and text. 
It can generate both text and images as output, analyze audio, and integrate with Discord.

Classes:
- GeminiClient: Main client for interacting with Google's Gemini API and managing processors

Dependencies:
- google.generativeai
- PIL
- requests
- logging
- dotenv

Related files:
- src/gemini/gemini_apis/: Low-level API functions
- src/gemini/gemini_hooks/: High-level workflow processors
- src/gemini/gemini_prompts/: Prompt templates
- src/gemini/gemini_utilities/: Utility functions
- src/discord/discord_client.py: Discord integration
"""

import os
import sys
import logging
from typing import Optional, Dict, Any, List, Union
from pathlib import Path

# Import the Google Generative AI client
import google.generativeai as genai
from google import genai as modern_genai

# Import the Discord client
try:
    # Try relative import first
    from ..discord.discord_client import DiscordClient
except ImportError:
    # Fall back to absolute import when run directly
    sys.path.insert(0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../..')))
    from src.discord.discord_client import DiscordClient

# Import our modular components
from src.gemini.gemini_apis.core_api import (
    send_to_discord,
    send_error_to_discord,
    generate_content,
    generate_image
)
from src.gemini.gemini_apis.audio_api import analyze_audio
from src.gemini.gemini_apis.image_api import analyze_image
from src.gemini.gemini_apis.multimodal_api import analyze_multimodal
from src.gemini.gemini_apis.chat_api import create_chat, send_message, get_chat_history
from src.gemini.gemini_apis.file_api import list_files, delete_file, upload_file

from src.gemini.gemini_hooks.audio_processor import AudioProcessor
from src.gemini.gemini_hooks.image_processor import ImageProcessor
from src.gemini.gemini_hooks.audio_to_image_processor import AudioToImageProcessor
from src.gemini.gemini_hooks.conversation_manager import ConversationManager

from src.gemini.gemini_utilities.file_utils import save_image

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for interacting with Google's Gemini API with Discord integration"""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash"):
        """
        Initialize the Gemini client with API key, configuration, and Discord integration.

        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY environment variable)
            model_name: Model name to use (default: gemini-2.0-flash)
        """
        # Use provided API key or get from environment
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key is required. Set GEMINI_API_KEY environment variable or pass to constructor.")

        # Initialize the client API
        self.client = modern_genai.Client(api_key=self.api_key)

        # Initialize Discord client
        self.discord_client = DiscordClient()

        # Model configuration
        self.model_name = model_name
        self.default_generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }

        # Initialize processors
        self.audio_processor = AudioProcessor(self.client)
        self.image_processor = ImageProcessor(self.client)
        self.audio_to_image_processor = AudioToImageProcessor(self.client)

        # Initialize chat
        self.chat = None

        # Initialize rate limiter for conversation manager
        from src.gemini.gemini_utilities.rate_limiter import RateLimiter
        rate_limiter = RateLimiter(
            max_calls_per_minute=60, max_calls_per_day=500)

        self.conversation_manager = ConversationManager(
            api_key=self.api_key,
            model_name=self.model_name,
            rate_limiter=rate_limiter
        )

        logger.info(f"GeminiClient initialized with model: {self.model_name}")

    def _send_to_discord(self, response: str, prompt: str = None, is_final: bool = False,
                         source: str = None, content_type: str = "text"):
        """
        Send a Gemini response to Discord.

        Args:
            response: The response from Gemini
            prompt: The prompt that was sent to Gemini
            is_final: Whether this is the final response
            source: Source information (e.g., file being analyzed)
            content_type: Type of content being processed (text, image, audio, etc.)
        """
        send_to_discord(
            discord_client=self.discord_client,
            response=response,
            prompt=prompt,
            is_final=is_final,
            source=source,
            content_type=content_type
        )

    def _send_error_to_discord(self, error: Exception, prompt: str = None):
        """
        Send an error to Discord safely without risking recursion.

        Args:
            error: The error that occurred
            prompt: The prompt that caused the error
        """
        send_error_to_discord(
            discord_client=self.discord_client,
            error=error,
            prompt=prompt
        )

    def generate_content(self, prompt: str, temperature: float = 0.7, system_instruction: Optional[str] = None) -> str:
        """
        Generate text based on a prompt and send the response to Discord.

        Args:
            prompt: Text prompt to generate content from
            temperature: Controls randomness (0.0-2.0)
            system_instruction: Optional instruction to guide the model's behavior

        Returns:
            Generated text
        """
        try:
            response_text = generate_content(
                client=self.client,
                model_name=self.model_name,
                prompt=prompt,
                temperature=temperature,
                system_instruction=system_instruction,
                max_output_tokens=self.default_generation_config["max_output_tokens"],
                top_p=self.default_generation_config["top_p"],
                top_k=self.default_generation_config["top_k"]
            )

            # Send to Discord
            self._send_to_discord(
                response=response_text,
                prompt=prompt,
                is_final=True,
                content_type="text"
            )

            return response_text
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            self._send_error_to_discord(e, prompt)
            raise

    def generate_image(self, prompt: str, temperature: float = 0.9):
        """
        Generate an image based on a text prompt and send the result to Discord.

        Args:
            prompt: Text description of the image to generate
            temperature: Controls randomness (0.0-2.0)

        Returns:
            Tuple of (response_text, image)
        """
        try:
            description_text, generated_image = generate_image(
                client=self.client,
                prompt=prompt,
                temperature=temperature
            )

            # Send description to Discord if available
            if description_text:
                self._send_to_discord(
                    response=description_text,
                    prompt=prompt,
                    is_final=False,
                    content_type="image"
                )

            return description_text, generated_image

        except Exception as e:
            logger.error(f"Error with image generation: {str(e)}")
            self._send_error_to_discord(e, prompt)

            # Create fallback image with error
            from src.gemini.gemini_apis.image_api import create_fallback_image
            fallback_image = create_fallback_image(
                error_message=str(e), color=(255, 0, 0))
            error_message = f"Failed to generate image: {str(e)}"

            return error_message, fallback_image

    def analyze_image(self, image_path_or_file, prompt: str, temperature: float = 0.4) -> str:
        """
        Analyze an image with an optional prompt for guidance and send results to Discord.

        Args:
            image_path_or_file: Path to image file or PIL Image object
            prompt: Text prompt to guide the analysis
            temperature: Controls randomness (0.0-2.0)

        Returns:
            Analysis text
        """
        try:
            response_text = analyze_image(
                client=self.client,
                image_path_or_file=image_path_or_file,
                prompt=prompt,
                temperature=temperature
            )

            # Get source info for logging
            source = image_path_or_file if isinstance(
                image_path_or_file, str) else "PIL Image"

            # Send to Discord
            self._send_to_discord(
                response=response_text,
                prompt=prompt,
                is_final=True,
                source=source,
                content_type="image analysis"
            )

            return response_text
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            self._send_error_to_discord(e, prompt)
            raise

    def analyze_audio(self, audio_path_or_file, prompt: str, temperature: float = 0.4) -> str:
        """
        Analyze audio content with a text prompt for guidance and send results to Discord.

        Args:
            audio_path_or_file: Path to audio file or BytesIO object
            prompt: Text prompt to guide the analysis
            temperature: Controls randomness (0.0-2.0)

        Returns:
            Analysis text
        """
        try:
            response_text = analyze_audio(
                client=self.client,
                audio_path_or_file=audio_path_or_file,
                prompt=prompt,
                temperature=temperature
            )

            # Get source info for logging
            source = audio_path_or_file if isinstance(
                audio_path_or_file, str) else "BytesIO Audio"

            # Send to Discord
            self._send_to_discord(
                response=response_text,
                prompt=prompt,
                is_final=True,
                source=source,
                content_type="audio analysis"
            )

            return response_text
        except Exception as e:
            logger.error(f"Error analyzing audio: {str(e)}")
            self._send_error_to_discord(e, prompt)
            raise

    def analyze_multimodal(self, contents, temperature: float = 0.4) -> str:
        """
        Analyze multiple types of content (text, images, audio) in a single request
        and send results to Discord.

        Args:
            contents: List of content items (text strings, images, file references)
            temperature: Controls randomness (0.0-2.0)

        Returns:
            Analysis text
        """
        try:
            response_text = analyze_multimodal(
                client=self.client,
                contents=contents,
                temperature=temperature
            )

            # Send to Discord
            from src.gemini.gemini_apis.multimodal_api import determine_content_type
            content_types = [determine_content_type(item) for item in contents]
            content_summary = f"multimodal analysis ({', '.join(content_types)})"

            self._send_to_discord(
                response=response_text,
                prompt=f"Analyzing {len(contents)} items: {content_summary}",
                is_final=True,
                content_type="multimodal"
            )

            return response_text
        except Exception as e:
            logger.error(f"Error with multimodal analysis: {str(e)}")
            self._send_error_to_discord(
                e, f"Multimodal analysis with {len(contents)} items")
            raise

    def create_chat(self, system_instruction: Optional[str] = None):
        """
        Create a new chat session with an optional system instruction.

        Args:
            system_instruction: Optional instruction to guide the model's behavior

        Returns:
            The chat object
        """
        self.chat = create_chat(
            client=self.client,
            model_name=self.model_name,
            system_instruction=system_instruction
        )
        return self.chat

    def send_message(self, text: str, stream: bool = False):
        """
        Send a message to the chat session and relay the response to Discord.

        Args:
            text: The message text to send
            stream: Whether to stream the response

        Returns:
            Chat response or stream
        """
        try:
            # Initialize chat if not already done
            if self.chat is None:
                self.create_chat()

            # Send message
            response = send_message(
                chat=self.chat,
                text=text,
                stream=stream
            )

            # Send to Discord for non-streaming responses
            if not stream:
                self._send_to_discord(
                    response=response.text,
                    prompt=text,
                    is_final=False,
                    content_type="chat"
                )

            return response

        except Exception as e:
            logger.error(f"Error sending chat message: {str(e)}")
            self._send_error_to_discord(e, text)
            raise

    def get_chat_history(self):
        """
        Get the history of the current chat session.

        Returns:
            List of chat messages
        """
        return get_chat_history(self.chat)

    # File management
    def list_files(self) -> List[Any]:
        """
        List all files uploaded to Gemini.

        Returns:
            List of file objects
        """
        return list_files(self.client)

    def delete_file(self, file_name: str) -> bool:
        """
        Delete a file from Gemini.

        Args:
            file_name: Name of the file to delete

        Returns:
            True if successful, False otherwise
        """
        return delete_file(self.client, file_name)

    def upload_file(self, file_path: str) -> Any:
        """
        Upload a file to Gemini.

        Args:
            file_path: Path to the file to upload

        Returns:
            File object reference
        """
        return upload_file(self.client, file_path)

    # Audio-to-image processing methods
    def process_audio_file(self, audio_path):
        """
        Process a single audio file through the entire pipeline:
        1. Analyze audio with Gemini
        2. Generate an image prompt
        3. Generate an image

        Args:
            audio_path: Path to the audio file

        Returns:
            Dictionary with results of the processing
        """
        return self.audio_to_image_processor.process_audio_file(audio_path)

    def process_multiple_files(self, audio_paths):
        """
        Process multiple audio files and send a summary to Discord

        Args:
            audio_paths: List of paths to audio files

        Returns:
            List of dictionaries with processing results
        """
        return self.audio_to_image_processor.process_multiple_files(audio_paths)

    def clean_output_directories(self):
        """
        Clean the output directories before processing files.
        """
        return self.audio_to_image_processor.clean_output_directories()

    def perform_multi_step_audio_analysis(self, audio_path):
        """
        Perform a four-step viral music analysis of an audio file:
        1. Step 1: Core Elements and Viral Hook Foundation - identifies genre, tempo, key, mood, instrumentation, and potential viral hooks
        2. Step 2: Sound Engineering, Techniques, and Trend Analysis - evaluates production quality, mix engineering, and trend alignment
        3. Step 3: Harmony, Melody, and Viral Hook Refinement - analyzes harmonic structure, melodic elements, and refines viral hook potential
        4. Step 4: Structure, Production, and Viral Hook Optimization - examines song structure, production techniques, and optimizes viral elements
        5. Final Analysis: Comprehensive merge of all analyses focused on viral content creation

        Args:
            audio_path: Path to the audio file

        Returns:
            Dictionary with all analyses and results, with focus on viral potential
        """
        return self.audio_to_image_processor.perform_multi_step_analysis(audio_path)


class AudioImageProcessor:
    """Legacy class for processing audio files and generating images, kept for backward compatibility.
    Uses AudioToImageProcessor internally for all operations."""

    def __init__(self, client):
        """
        Initialize the processor with client and output directories

        Args:
            client: Gemini client instance
        """
        self.client = client
        self.processor = AudioToImageProcessor(client)

        # Set up directories for backward compatibility
        self.image_dir = self.processor.image_processor.image_dir
        self.prompt_dir = self.processor.image_processor.prompt_dir
        self.analysis_dir = self.processor.audio_processor.analysis_dir

        logger.info("AudioImageProcessor initialized (legacy class)")

    def process_audio_file(self, audio_path):
        """
        Process a single audio file through the processor pipeline

        Args:
            audio_path: Path to the audio file

        Returns:
            Dictionary with results of the processing
        """
        return self.processor.process_audio_file(audio_path)

    def process_multiple_files(self, audio_paths):
        """
        Process multiple audio files

        Args:
            audio_paths: List of paths to audio files

        Returns:
            List of dictionaries with processing results
        """
        return self.processor.process_multiple_files(audio_paths)


# Example usage
if __name__ == "__main__":
    # Create the integrated client
    client = GeminiClient()

    # Example: Generate and send content to Discord
    response = client.generate_content(
        "Explain how large language models like Gemini work in 3 paragraphs"
    )

    print("Response sent to Discord successfully!")
