#!/usr/bin/env python
"""
test_revised_analysis.py - Test script for generating revised analysis from refined analysis

This script demonstrates the process of revising the final analysis based on the refined analysis.
The process includes:
1. Checking for existing final analysis and refined analysis files
2. Reading both analyses
3. Generating a revised analysis that incorporates corrections and verified details
4. Using the revised analysis for image generation

This demonstrates the complete pipeline from audio analysis to accurate image generation.
"""

import os
import sys
import logging
import time
import json
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
    Main function to demonstrate the revised analysis generation process.
    """
    # Check if API key is set
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error(
            "GEMINI_API_KEY environment variable is not set. Please set it before running this script.")
        sys.exit(1)

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

    # Check if we have existing analyses
    analysis_dir = Path("output/analysis")
    final_analysis_path = analysis_dir / f"{audio_path.stem}_analysis.txt"
    refined_analysis_path = analysis_dir / \
        f"{audio_path.stem}_refined_analysis.txt"

    if not final_analysis_path.exists():
        logger.error(
            f"No existing final analysis found at {final_analysis_path}")
        logger.info(
            "Please run the full analysis pipeline first using test_refinement.py")
        sys.exit(1)

    if not refined_analysis_path.exists():
        logger.error(
            f"No existing refined analysis found at {refined_analysis_path}")
        logger.info(
            "Please run the refinement step first using test_refinement.py")
        sys.exit(1)

    # Initialize the GeminiClient and AudioToImageProcessor
    from src.gemini.gemini_client import GeminiClient
    from src.gemini.gemini_hooks.audio_to_image_processor import AudioToImageProcessor

    client = GeminiClient(api_key=api_key)
    processor = AudioToImageProcessor(client=client)

    # Read the final analysis and refined analysis
    final_analysis = final_analysis_path.read_text(encoding="utf-8")
    refined_analysis = refined_analysis_path.read_text(encoding="utf-8")

    logger.info(f"Read final analysis from {final_analysis_path}")
    logger.info(f"Read refined analysis from {refined_analysis_path}")

    # Generate the revised analysis
    logger.info("Generating revised analysis...")
    revision_result = processor.revise_final_analysis(
        audio_path=audio_path,
        final_analysis=final_analysis,
        refined_analysis=refined_analysis
    )

    if revision_result.get("revision_success", False):
        revised_analysis_path = revision_result.get("revised_analysis_path")
        logger.info(
            f"Revised analysis generated successfully: {revised_analysis_path}")

        # Read the revised analysis
        revised_analysis = Path(
            revised_analysis_path).read_text(encoding="utf-8")

        # Generate image prompt from the revised analysis
        logger.info("Generating image prompt from revised analysis...")
        prompt_result = processor.generate_image_prompt(
            audio_path=audio_path,
            analysis_text=revised_analysis
        )

        if prompt_result.get("prompt_success", False):
            prompt_path = prompt_result.get("prompt_path")
            logger.info(f"Image prompt generated successfully: {prompt_path}")

            # Read the prompt file
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt_data = json.load(f)

            # Generate the image
            logger.info("Generating image from prompt...")
            image_result = processor.generate_image(
                audio_path=audio_path,
                prompt_data=prompt_data
            )

            if image_result.get("image_success", False):
                image_path = image_result.get("image_path")
                logger.info(f"Image generated successfully: {image_path}")
                print("\nComplete pipeline executed successfully:")
                print(f"1. Final analysis: {final_analysis_path}")
                print(f"2. Refined analysis: {refined_analysis_path}")
                print(f"3. Revised analysis: {revised_analysis_path}")
                print(f"4. Image prompt: {prompt_path}")
                print(f"5. Generated image: {image_path}")
            else:
                logger.error(
                    f"Image generation failed: {image_result.get('image_error')}")
        else:
            logger.error(
                f"Image prompt generation failed: {prompt_result.get('prompt_error')}")
    else:
        logger.error(
            f"Revision failed: {revision_result.get('revision_error')}")

    # Print a summary
    print("\n--- PROCESS SUMMARY ---")
    print("1. Final analysis -> Contains comprehensive information about the audio")
    print("2. Refined analysis -> Critical verification of technical details and accuracy")
    print("3. Revised analysis -> Final analysis updated with verified and corrected information")
    print("4. Image prompt -> Generated from the revised analysis for maximum accuracy")
    print("5. Image -> Visual representation based on the most accurate analysis")
    print("--- END SUMMARY ---\n")


if __name__ == "__main__":
    main()
