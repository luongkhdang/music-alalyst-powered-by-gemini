"""
gemini_apis/audio_api.py - Audio processing and analysis API for Gemini

Provides functions for processing and analyzing audio files:
- analyze_audio(client, audio_path_or_file, prompt, temperature): Analyzes audio with Gemini
- create_audio_analysis_prompt(): Returns a detailed prompt for comprehensive audio analysis

Related files:
- src/gemini/gemini_client.py: Main client that uses these API functions
- src/gemini/gemini_apis/core_api.py: Core API functions used by this module
"""

import os
import tempfile
import logging
from typing import Union, Optional, Tuple
from io import BytesIO
from pathlib import Path
from google.genai import types

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_audio_analysis_prompt() -> str:
    """
    Create a comprehensive prompt for audio analysis.

    Returns:
        str: Detailed prompt for analyzing audio files
    """
    return """
    Analyze this audio file in comprehensive detail. Please cover:
    
    1. TECHNICAL ASPECTS:
       - Genre classification and sub-genres
       - Tempo (BPM) and rhythm patterns
       - Key signature and chord progressions
       - Production quality and techniques
       - Instrument identification
       
    2. EMOTIONAL QUALITIES:
       - Overall mood and atmosphere
       - Emotional journey throughout the track
       - Intensity curves and dynamic range
       - Psychological impact on listeners
       
    3. VISUAL ASSOCIATIONS:
       - Color palette that represents the sound
       - Visual scenes or imagery evoked
       - Textures and physical sensations suggested
       - Environmental settings that match the audio
       
    4. CREATIVE DIRECTION:
       - Artistic intentions behind production choices
       - Cultural or historical references
       - Innovative or unique elements
       - Potential use cases (film, advertising, etc.)
       
    Provide substantive detail in each section. This analysis will be used to guide visual art generation.
    """


def analyze_audio(client, audio_path_or_file: Union[str, BytesIO, Path],
                  prompt: Optional[str] = None,
                  temperature: float = 0.4,
                  model_name: str = "gemini-2.0-flash") -> str:
    """
    Analyze audio content with a text prompt for guidance.

    Args:
        client: Initialized Gemini client instance
        audio_path_or_file: Path to audio file, Path object, or BytesIO object
        prompt: Text prompt to guide the analysis (if None, uses default analysis prompt)
        temperature: Controls randomness (0.0-2.0)
        model_name: Model name to use (default: gemini-2.0-flash)

    Returns:
        str: Analysis text from Gemini
    """
    # Use default prompt if none provided
    if prompt is None:
        prompt = create_audio_analysis_prompt()

    # Convert Path to string if needed
    if isinstance(audio_path_or_file, Path):
        audio_path_or_file = str(audio_path_or_file)

    # Upload the file using the modern API if it's a path
    if isinstance(audio_path_or_file, str):
        uploaded_file = client.files.upload(
            file=audio_path_or_file)

        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=8192
        )

        response = client.models.generate_content(
            model=model_name,
            contents=[prompt, uploaded_file],
            config=config
        )

        return response.text
    else:
        # For BytesIO objects, create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            if isinstance(audio_path_or_file, BytesIO):
                temp_file.write(audio_path_or_file.getvalue())
            else:
                temp_file.write(audio_path_or_file)
            temp_path = temp_file.name

        try:
            uploaded_file = client.files.upload(file=temp_path)

            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=8192
            )

            response = client.models.generate_content(
                model=model_name,
                contents=[prompt, uploaded_file],
                config=config
            )

            return response.text
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
