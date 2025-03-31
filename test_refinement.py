#!/usr/bin/env python
"""
test_refinement.py - Test script for the refinement step in audio analysis

This script demonstrates how to use the refinement step in the audio-to-image processing workflow.
The refinement step has Gemini act as a critical Musical Foundation Specialist to verify 
the accuracy of the final analysis.
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def main():
    """
    Main function to demonstrate the refinement step in audio analysis.
    """
    # Import the necessary modules
    from src.gemini.gemini_client import GeminiClient
    from src.gemini.gemini_hooks.audio_to_image_processor import AudioToImageProcessor

    # Check if API key is set
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error(
            "GEMINI_API_KEY environment variable is not set. Please set it before running this script.")
        sys.exit(1)

    # Initialize the Gemini client
    logger.info("Initializing Gemini client...")
    client = GeminiClient(api_key=api_key)

    # Initialize the audio-to-image processor
    logger.info("Initializing AudioToImageProcessor...")
    processor = AudioToImageProcessor(client=client)

    # Path to the audio file to analyze
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
    else:
        # Default test audio file (update this path as needed)
        audio_path = "samples/test_audio.mp3"

    audio_path = Path(audio_path)
    if not audio_path.exists():
        logger.error(f"Audio file not found: {audio_path}")
        logger.info(
            "Please provide a valid audio file path as an argument, or update the default path in the script.")
        sys.exit(1)

    logger.info(f"Analyzing audio file: {audio_path}")

    # Process the audio file
    # This will perform the full analysis pipeline including the refinement step
    result = processor.process_audio_file(audio_path)

    # Check if the analysis was successful
    if result["analysis_success"]:
        logger.info("Analysis completed successfully!")

        # Check if refined analysis was generated
        if result.get("refined_analysis_path"):
            logger.info(
                f"Refined analysis path: {result['refined_analysis_path']}")

            # Print a snippet of the refined analysis
            refined_path = Path(result["refined_analysis_path"])
            if refined_path.exists():
                refined_text = refined_path.read_text(encoding="utf-8")
                print("\n--- SNIPPET FROM REFINED ANALYSIS ---")
                print(refined_text[:500] + "...")
                print("--- END SNIPPET ---\n")

        # Check if image was generated
        if result["image_success"]:
            logger.info(
                f"Image generated successfully: {result['image_path']}")
        else:
            logger.error(
                f"Image generation failed: {result.get('image_error', 'Unknown error')}")
    else:
        logger.error(
            f"Analysis failed: {result.get('analysis_error', 'Unknown error')}")


if __name__ == "__main__":
    main()
