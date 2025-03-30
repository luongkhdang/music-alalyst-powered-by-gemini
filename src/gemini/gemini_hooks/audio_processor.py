"""
gemini_hooks/audio_processor.py - Audio processing workflows for Gemini

Provides high-level functions for audio processing workflows:
- AudioProcessor: A class that handles the audio processing pipeline
  - analyze_audio(audio_path): Analyzes audio and saves results
  - generate_image_prompt(analysis, audio_name): Creates image prompts from audio analysis
  - process_audio_file(audio_path): Processes a single audio file through the full pipeline

Related files:
- src/gemini/gemini_client.py: Main client that uses this processor
- src/gemini/gemini_apis/audio_api.py: Lower-level audio API functions
- src/gemini/gemini_apis/image_api.py: Used for generating images
"""

import os
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

from src.gemini.gemini_apis.audio_api import analyze_audio, create_audio_analysis_prompt
from src.gemini.gemini_utilities.file_utils import save_text, save_json, ensure_directory

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioProcessor:
    """Handles audio processing workflows for the Gemini client"""

    def __init__(self, client, output_dir: str = "output"):
        """
        Initialize the audio processor with client and output directories

        Args:
            client: Gemini client instance
            output_dir: Base directory for all outputs
        """
        self.client = client
        self.output_dir = Path(output_dir)
        self.analysis_dir = self.output_dir / "analysis"

        # Ensure directories exist
        ensure_directory(self.analysis_dir)

        logger.info("AudioProcessor initialized")

    def analyze_audio(self, audio_path: Union[str, Path]) -> str:
        """
        Analyze an audio file using Gemini API

        Args:
            audio_path: Path to the audio file

        Returns:
            Analysis text
        """
        audio_path = Path(audio_path)
        analysis_path = self.analysis_dir / f"{audio_path.stem}_analysis.txt"

        # Check if analysis already exists
        if analysis_path.exists():
            logger.info(
                f"Analysis already exists for {audio_path.name}, loading from file")
            return self.load_analysis(audio_path.stem)

        logger.info(f"Analyzing audio: {audio_path.name}")

        # Generate prompt for analysis
        prompt = (
            "Analyze this audio file with meticulous detail, targeting a world-class producer’s perspective. Please structure your analysis in these sections:\n\n"
            "1. TECHNICAL ASPECTS:\n"
            "   - Genre & Sub-genre: Identify the primary genre (e.g., techno, trap) and micro-genre influences (e.g., industrial techno, melodic trap), noting stylistic markers (e.g., 909 kicks, triplet hi-hats).\n"
            "   - Tempo & Rhythm: Measure exact BPM (e.g., 126.3 BPM), detect variations (e.g., halftime at 1:30), and analyze rhythmic complexity (e.g., polyrhythms, swing percentage).\n"
            "   - Key Signature & Tonality: Pinpoint the key (e.g., F# Minor), detect modulations (e.g., to D Major at 2:00), and assess tonal character (e.g., pentatonic lean, microtonal hints).\n"
            "   - Production Quality: Evaluate mix clarity (e.g., -8 LUFS, 8 dB dynamic range), stereo imaging (e.g., 60% width at 1 kHz), and mastering polish (e.g., -0.2 dBTP ceiling).\n"
            "   - Instrumentation & Sound Design: Catalog instruments (e.g., Juno-106 sawtooth, 808 sub), detail synthesis (e.g., 20% detune, 50 ms ADSR decay), and note FX (e.g., 1/8th-note delay, 30% wet).\n\n"
            "2. EMOTIONAL QUALITIES:\n"
            "   - Overall Mood: Define the dominant emotion (e.g., melancholic euphoria) and psychoacoustic drivers (e.g., low-end warmth at 60 Hz, high shimmer at 8 kHz).\n"
            "   - Emotional Journey: Map intensity arcs (e.g., tension at 0:45-1:15, release at 1:30), pinpoint pivot points (e.g., drop at 2:00 shifts to hope), and quantify energy (e.g., RMS -12 dB to -6 dB).\n"
            "   - Intensity Curves: Graph dynamic shifts (e.g., 4 dB swell over 16 bars), harmonic tension (e.g., dissonance peaks at 1:45), and timbral evolution (e.g., filter opens 500 Hz to 5 kHz).\n\n"
            "3. VISUAL ASSOCIATIONS:\n"
            "   - Color Palette: Assign hues to frequencies (e.g., 40-120 Hz = deep indigo, 2-8 kHz = neon cyan), moods (e.g., tension = rust red), and textures (e.g., grit = matte gray).\n"
            "   - Imagery & Scenes: Evoke specific visuals (e.g., rain-slicked neon cityscape, pulsing fractal void) tied to rhythm (e.g., 4/4 = gridlines) and melody (e.g., arpeggio = cascading lights).\n"
            "   - Textures & Materials: Suggest tactile qualities (e.g., metallic sheen for hi-hats, velvet fog for pads) and environmental vibes (e.g., industrial decay, cosmic ether).\n\n"
            "4. CREATIVE DIRECTION:\n"
            "   - Artistic Intentions: Infer producer goals (e.g., nostalgic rave revival, futuristic dystopia) via sonic choices (e.g., bit-crushed snare, detuned lead).\n"
            "   - Cultural References: Link to influences (e.g., 90s Detroit techno, cyberpunk anime OSTs) and subcultural cues (e.g., glitch art, vaporwave aesthetics).\n"
            "   - Potential Uses: Propose contexts (e.g., VR club scene soundtrack, TikTok glitch-dance trend, avant-garde film score) with platform-specific tweaks (e.g., 15s loop at 1:00-1:15).\n\n"
            "Provide precise, quantifiable details (e.g., frequencies, timestamps, dB levels) in each section, synthesizing a multi-dimensional analysis that bridges sound and vision."
        )

        # Perform the analysis using the audio_api module
        try:
            from src.gemini.gemini_apis.audio_api import analyze_audio

            response = analyze_audio(
                client=self.client,
                audio_path_or_file=audio_path,
                prompt=prompt,
                temperature=0.4
            )

            # Save the analysis
            save_text(response, analysis_path)
            logger.info(f"Saved analysis to {analysis_path}")

            return response
        except Exception as e:
            logger.error(f"Error analyzing audio {audio_path.name}: {str(e)}")
            raise

    def load_analysis(self, filename_stem: str) -> str:
        """
        Load an existing analysis from file

        Args:
            filename_stem: Base filename without extension

        Returns:
            Analysis text content
        """
        analysis_path = self.analysis_dir / f"{filename_stem}_analysis.txt"

        if not analysis_path.exists():
            logger.error(f"Analysis file not found: {analysis_path}")
            raise FileNotFoundError(
                f"Analysis file not found: {analysis_path}")

        try:
            analysis_text = analysis_path.read_text(encoding='utf-8')
            return analysis_text
        except Exception as e:
            logger.error(
                f"Error loading analysis from {analysis_path}: {str(e)}")
            raise

    def generate_image_prompt(self, analysis: str, audio_name: str) -> Dict[str, Any]:
        """
        Generate an image prompt based on audio analysis

        Args:
            analysis: Analysis text from Gemini
            audio_name: Name of the audio file

        Returns:
            Dict: Image generation prompt data
        """
        logger.info(f"Generating image prompt for {audio_name}")

        # Template for generating image prompts from audio analysis
        prompt_instruction = """
        Based on the provided audio analysis, craft a highly detailed text prompt for generating an image that encapsulates the song’s essence and vibe, designed for a world-class producer’s visual imagination. The prompt must be vivid, technically informed, and evocative, including:
        Primary Scene or Subject: Define a central focus (e.g., a lone figure in a neon-drenched alley, a crystalline orb pulsing in a void) tied to the song’s core mood and structure.
        Color Palette & Mood: Specify dominant hues (e.g., indigo gradients, acid green accents) and tonal mood (e.g., brooding with flickers of hope), reflecting frequency mappings and emotional arcs.
        Lighting & Atmosphere: Detail light sources (e.g., cold LED glow at 4500K, flickering strobe at 120 BPM) and environmental feel (e.g., dense fog at 80% opacity, crystalline clarity).
        Style: Recommend an art style (e.g., hyper-realistic 3D render, glitchy cyber-surrealism, abstract vector minimalism) aligned with production quality and cultural references.
        Unique Visual Elements: Incorporate specific details (e.g., fractal waveforms pulsing at 126 BPM, metallic shards reflecting 8 kHz hi-hats) mirroring instrumentation and sound design.
        Integrate technical audio cues (e.g., tempo synced motion, harmonic color shifts) and emotional resonance (e.g., tension as angular shadows) into the visual narrative. 
        
        Format your response as a JSON object with this structure:
        {
            prompt: The complete image generation prompt (detailed, concise, max 200 words),
            mood: Primary mood distilled from the song’s emotional qualities,
            colors: [list, of, dominant, colors, with, hex, codes],
            style: Suggested art style with technical justification
        }
        """

        # Generate the prompt using Gemini
        prompt_response = self.client.generate_content(
            prompt=f"Audio Analysis:\n{analysis}\n\n{prompt_instruction}",
            temperature=0.7
        )

        # Extract JSON from the response
        try:
            # Find JSON within the response if it's not pure JSON
            json_start = prompt_response.find('{')
            json_end = prompt_response.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = prompt_response[json_start:json_end]
                prompt_data = json.loads(json_str)
            else:
                # Fallback if no JSON is found
                logger.warning(
                    f"Could not extract JSON from response for {audio_name}")
                prompt_data = {
                    # Use first 500 chars as prompt
                    "prompt": prompt_response[:500],
                    "mood": "unknown",
                    "colors": ["vibrant"],
                    "style": "modern"
                }
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON in prompt response for {audio_name}")
            # Create a basic prompt from the response
            prompt_data = {
                # Use first 500 chars as prompt
                "prompt": prompt_response[:500],
                "mood": "unknown",
                "colors": ["vibrant"],
                "style": "modern"
            }

        # Add metadata
        prompt_data["audio_file"] = audio_name
        prompt_data["timestamp"] = datetime.now().isoformat()

        return prompt_data
