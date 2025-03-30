#!/usr/bin/env python3
"""
main.py - MP3 to Image Generation Pipeline

This script processes MP3 files from the data_source folder:
1. Analyzes the audio using Gemini API
2. Generates a JSON prompt describing the vibe of the song
3. Creates an image based on that prompt
4. Saves the image to output/images/ directory
5. Sends all Gemini responses to Discord for real-time monitoring

Dependencies:
- os, json, datetime
- google.generativeai
- PIL
- src.gemini.gemini_client
- src.discord.discord_client

Related files: 
- src/gemini/gemini_client.py
- src/discord/discord_client.py
"""

import os
import json
import logging
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, List

# Import the necessary modules
try:
    # When run from root directory
    from src.gemini.gemini_client import GeminiClient, AudioImageProcessor
    from src.discord.discord_client import DiscordClient
except ModuleNotFoundError:
    # When run directly from src directory
    sys.path.insert(0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')))
    from src.gemini.gemini_client import GeminiClient, AudioImageProcessor
    from src.discord.discord_client import DiscordClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AudioImageGenerator:
    """Pipeline for generating images from audio files using Gemini API with Discord integration"""

    def __init__(self, client=None):
        """
        Initialize the generator with client and processor

        Args:
            client: Optional GeminiClient instance
        """
        # Initialize Gemini client
        self.client = client or GeminiClient()

        # Initialize the audio processor from gemini_client.py
        self.processor = AudioImageProcessor(client=self.client)

        # Set up data directory
        self.data_dir = Path("data_source")

        # Get a reference to the Discord client
        self.discord_client = self.client.discord_client or DiscordClient()

        logger.info("AudioImageGenerator initialized with Discord integration")

    def get_audio_files(self) -> List[Path]:
        """
        Get all MP3 files from the data source directory

        Returns:
            List of paths to MP3 files
        """
        mp3_files = list(self.data_dir.glob("*.mp3"))
        logger.info(f"Found {len(mp3_files)} MP3 files in data_source folder")
        return mp3_files

    def clean_output_directories(self):
        """
        Clean the output directories before processing files.
        This is optional and only used when explicitly requested.
        """
        for path in [
            self.processor.image_dir,
            self.processor.prompt_dir,
            self.processor.analysis_dir
        ]:
            # Keep the directory but delete its contents
            if path.exists():
                for file in path.glob("*"):
                    file.unlink()
                logger.info(f"Cleaned directory: {path}")

        logger.info("Output directories cleaned")

    def process_audio_file(self, audio_path: Path) -> Dict[str, Any]:
        """
        Process a single audio file through the processor pipeline

        Args:
            audio_path: Path to the audio file

        Returns:
            Dictionary with results of the processing
        """
        # Simply delegate to the processor
        return self.processor.process_audio_file(audio_path)

    def process_all(self, clean_first=False) -> List[Dict[str, Any]]:
        """
        Process all MP3 files in the data source directory

        Args:
            clean_first: Whether to clean output directories before processing

        Returns:
            List of dictionaries with processing results
        """
        # Clean output directories if requested
        if clean_first:
            self.clean_output_directories()

        # Get all audio files
        audio_files = self.get_audio_files()

        # Process all files through the processor
        return self.processor.process_multiple_files(audio_files)


def main():
    """Main function to run the audio processing pipeline"""
    parser = argparse.ArgumentParser(
        description="MP3 to Image Generation Pipeline with Discord Integration")
    parser.add_argument(
        "--file", help="Process a single MP3 file from data_source folder")
    parser.add_argument("--all", action="store_true",
                        help="Process all MP3 files in data_source folder")
    parser.add_argument("--clean", action="store_true",
                        help="Clean output directories before processing")

    args = parser.parse_args()

    # Initialize the AudioImageGenerator
    generator = AudioImageGenerator()

    if args.file:
        # Process a single file
        audio_path = Path("data_source") / args.file
        if not audio_path.exists():
            logger.error(f"File not found: {audio_path}")
            return

        result = generator.process_audio_file(audio_path)
        print(json.dumps(result, indent=2))

    elif args.all:
        # Process all files
        results = generator.process_all(clean_first=args.clean)
        print(f"Processed {len(results)} files")

    else:
        # Show usage
        parser.print_help()


if __name__ == "__main__":
    main()
