#!/usr/bin/env python
"""
test_5_step_refinery.py - Test script for the 5-step refinery process in audio analysis

This script demonstrates how to use the 5-step refinery process for audio analysis.
Each step uses a specialized analyst to verify different aspects of the audio:
1. Musical Foundation Specialist: Verifies genre, tempo, key, mood, instrumentation, hooks
2. Engineering Specialist: Verifies frequency balance, stereo imaging, transients, production techniques
3. Harmony & Melody Specialist: Verifies chord progressions, melodic lines, trend alignment
4. Structure Specialist: Verifies arrangement, texture, production polish
5. Critical Evaluator: Verifies critiques and improvement suggestions

Finally, a Summary and Validation Expert cross-checks facts, resolves discrepancies, 
and distills the results into a final polished summary.
"""

import os
import sys
import logging
import time
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Constants
RATE_LIMIT_PAUSE = 5  # seconds to pause between API calls


def perform_5_step_refinery(audio_path: Path, final_analysis: str) -> Dict[str, Any]:
    """
    Perform the 5-step refinery process on an audio analysis.

    Args:
        audio_path: Path to the audio file being analyzed
        final_analysis: The final analysis text to refine

    Returns:
        Dictionary with paths to all refinery analysis files
    """
    from src.gemini.gemini_client import GeminiClient
    from src.gemini.gemini_prompts import (
        get_refinery_analyst1_prompt,
        get_refinery_analyst2_prompt,
        get_refinery_analyst3_prompt,
        get_refinery_analyst4_prompt,
        get_refinery_analyst5_prompt,
        get_final_refinery_prompt
    )

    # Initialize the Gemini client
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in environment")

    client = GeminiClient(api_key=api_key)

    # Set up output directory
    output_dir = Path("output/refinery")
    output_dir.mkdir(exist_ok=True, parents=True)

    # Dictionary to store results
    results = {
        "analyst1_output_path": None,
        "analyst2_output_path": None,
        "analyst3_output_path": None,
        "analyst4_output_path": None,
        "analyst5_output_path": None,
        "final_refinery_output_path": None
    }

    try:
        # Step 1: Musical Foundation Specialist
        logger.info("Running Refinery Analyst 1: Musical Foundation Specialist")
        prompt1 = get_refinery_analyst1_prompt(final_analysis)
        analyst1_output = client.analyze_audio(
            audio_path_or_file=audio_path,
            prompt=prompt1,
            temperature=0.3
        )

        # Save the output
        analyst1_path = output_dir / f"{audio_path.stem}_analyst1_output.txt"
        analyst1_path.write_text(analyst1_output, encoding="utf-8")
        logger.info(f"Analyst 1 output saved to {analyst1_path}")
        results["analyst1_output_path"] = str(analyst1_path)

        # Pause to respect API rate limits
        time.sleep(RATE_LIMIT_PAUSE)

        # Step 2: Engineering Specialist
        logger.info("Running Refinery Analyst 2: Engineering Specialist")
        prompt2 = get_refinery_analyst2_prompt(final_analysis)
        analyst2_output = client.analyze_audio(
            audio_path_or_file=audio_path,
            prompt=prompt2,
            temperature=0.3
        )

        # Save the output
        analyst2_path = output_dir / f"{audio_path.stem}_analyst2_output.txt"
        analyst2_path.write_text(analyst2_output, encoding="utf-8")
        logger.info(f"Analyst 2 output saved to {analyst2_path}")
        results["analyst2_output_path"] = str(analyst2_path)

        # Pause to respect API rate limits
        time.sleep(RATE_LIMIT_PAUSE)

        # Step 3: Harmony and Melody Specialist
        logger.info("Running Refinery Analyst 3: Harmony and Melody Specialist")
        prompt3 = get_refinery_analyst3_prompt(final_analysis)
        analyst3_output = client.analyze_audio(
            audio_path_or_file=audio_path,
            prompt=prompt3,
            temperature=0.3
        )

        # Save the output
        analyst3_path = output_dir / f"{audio_path.stem}_analyst3_output.txt"
        analyst3_path.write_text(analyst3_output, encoding="utf-8")
        logger.info(f"Analyst 3 output saved to {analyst3_path}")
        results["analyst3_output_path"] = str(analyst3_path)

        # Pause to respect API rate limits
        time.sleep(RATE_LIMIT_PAUSE)

        # Step 4: Structure Specialist
        logger.info("Running Refinery Analyst 4: Structure Specialist")
        prompt4 = get_refinery_analyst4_prompt(final_analysis)
        analyst4_output = client.analyze_audio(
            audio_path_or_file=audio_path,
            prompt=prompt4,
            temperature=0.3
        )

        # Save the output
        analyst4_path = output_dir / f"{audio_path.stem}_analyst4_output.txt"
        analyst4_path.write_text(analyst4_output, encoding="utf-8")
        logger.info(f"Analyst 4 output saved to {analyst4_path}")
        results["analyst4_output_path"] = str(analyst4_path)

        # Pause to respect API rate limits
        time.sleep(RATE_LIMIT_PAUSE)

        # Step 5: Critical Evaluator
        logger.info("Running Refinery Analyst 5: Critical Evaluator")
        prompt5 = get_refinery_analyst5_prompt(final_analysis)
        analyst5_output = client.analyze_audio(
            audio_path_or_file=audio_path,
            prompt=prompt5,
            temperature=0.3
        )

        # Save the output
        analyst5_path = output_dir / f"{audio_path.stem}_analyst5_output.txt"
        analyst5_path.write_text(analyst5_output, encoding="utf-8")
        logger.info(f"Analyst 5 output saved to {analyst5_path}")
        results["analyst5_output_path"] = str(analyst5_path)

        # Pause to respect API rate limits
        time.sleep(RATE_LIMIT_PAUSE)

        # Final Refinery: Summary and Validation Expert
        logger.info("Running Final Refinery: Summary and Validation Expert")

        # Read the outputs from all analysts
        analyst1_output = analyst1_path.read_text(encoding="utf-8")
        analyst2_output = analyst2_path.read_text(encoding="utf-8")
        analyst3_output = analyst3_path.read_text(encoding="utf-8")
        analyst4_output = analyst4_path.read_text(encoding="utf-8")
        analyst5_output = analyst5_path.read_text(encoding="utf-8")

        # Generate the final refinery prompt
        final_prompt = get_final_refinery_prompt(
            analyst1_output=analyst1_output,
            analyst2_output=analyst2_output,
            analyst3_output=analyst3_output,
            analyst4_output=analyst4_output,
            analyst5_output=analyst5_output,
            final_analysis=final_analysis
        )

        # Generate the final refinery output
        final_refinery_output = client.generate_content(
            prompt=final_prompt,
            temperature=0.4
        )

        # Save the output
        final_refinery_path = output_dir / \
            f"{audio_path.stem}_final_refinery_output.txt"
        final_refinery_path.write_text(final_refinery_output, encoding="utf-8")
        logger.info(f"Final refinery output saved to {final_refinery_path}")
        results["final_refinery_output_path"] = str(final_refinery_path)

        return results

    except Exception as e:
        logger.exception(f"Error in 5-step refinery process: {str(e)}")
        return results


def main():
    """
    Main function to demonstrate the 5-step refinery process.
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

    # Check if we have an existing final analysis
    analysis_dir = Path("output/analysis")
    final_analysis_path = analysis_dir / f"{audio_path.stem}_analysis.txt"

    if not final_analysis_path.exists():
        # We need to generate a final analysis first
        logger.info(
            f"No existing final analysis found at {final_analysis_path}")
        logger.info(
            "Please run the full analysis pipeline first using test_refinement.py")
        sys.exit(1)

    # Read the final analysis
    final_analysis = final_analysis_path.read_text(encoding="utf-8")
    logger.info(f"Read final analysis from {final_analysis_path}")

    # Perform the 5-step refinery process
    results = perform_5_step_refinery(audio_path, final_analysis)

    # Print a summary
    logger.info("5-step refinery process completed:")
    for key, value in results.items():
        if value:
            logger.info(f"  {key}: {value}")

    # If we have a final refinery output, print a snippet
    final_refinery_path = results.get("final_refinery_output_path")
    if final_refinery_path:
        path = Path(final_refinery_path)
        if path.exists():
            final_text = path.read_text(encoding="utf-8")
            print("\n--- SNIPPET FROM FINAL REFINERY OUTPUT ---")
            print(final_text[:500] + "...")
            print("--- END SNIPPET ---\n")


if __name__ == "__main__":
    main()
