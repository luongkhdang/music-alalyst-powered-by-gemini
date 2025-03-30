#!/usr/bin/env python3
"""
debug_client.py - Test script for the multi-step audio analysis

Tests the five-step analysis process for audio files:
1. Musical Foundation and Hook Analysis
2. Sound Engineering and Production Techniques
3. Harmony, Melody, and Trend Alignment
4. Structure and Production Optimization
5. Critical Evaluation and Improvement Suggestions
6. Final Integrated Analysis

Usage:
    python debug_client.py --multi-step-analysis PATH_TO_AUDIO_FILE
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Import the Gemini client
from src.gemini.gemini_client import GeminiClient

# Create a client instance
client = GeminiClient()

# Simple helper function to save the results


def save_results(results, filename):
    """Save results to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        # Create a serializable version of the results
        serializable = {}
        for key, value in results.items():
            if isinstance(value, Path):
                serializable[key] = str(value)
            else:
                serializable[key] = value
        json.dump(serializable, f, indent=2)
    print(f"Saved results to {filename}")

# Test the multi-step analysis


def test_multi_step_analysis(audio_file_path=None):
    """Test the multi-step analysis functionality"""
    print("Testing multi-step audio analysis...")

    # Get the first audio file from data_source if not specified
    if audio_file_path:
        audio_file = Path(audio_file_path)
    else:
        audio_file = next(Path("data_source").glob("*.mp3"))

    print(f"Using audio file: {audio_file}")

    # Perform the multi-step analysis
    results = client.perform_multi_step_audio_analysis(audio_file)

    # Save the results
    output_file = Path("output") / "debug_multi_step_analysis.json"

    # Create summary of the results
    summary = {
        "audio_file": results["audio_file"],
        "success": results["success"],
        "step1_length": len(results["step1_analysis"]) if results.get("step1_analysis") else 0,
        "step2_length": len(results["step2_analysis"]) if results.get("step2_analysis") else 0,
        "step3_length": len(results["step3_analysis"]) if results.get("step3_analysis") else 0,
        "step4_length": len(results["step4_analysis"]) if results.get("step4_analysis") else 0,
        "step5_length": len(results["step5_analysis"]) if results.get("step5_analysis") else 0,
        "final_length": len(results["final_analysis"]) if results.get("final_analysis") else 0,
    }

    # Print the summary
    print("\nAnalysis Results Summary:")
    print(f"Audio File: {summary['audio_file']}")
    print(f"Success: {summary['success']}")
    print(f"Step 1 Analysis Length: {summary['step1_length']} characters")
    print(f"Step 2 Analysis Length: {summary['step2_length']} characters")
    print(f"Step 3 Analysis Length: {summary['step3_length']} characters")
    print(f"Step 4 Analysis Length: {summary['step4_length']} characters")
    print(f"Step 5 Analysis Length: {summary['step5_length']} characters")
    print(f"Final Analysis Length: {summary['final_length']} characters")

    # Save just the summary
    save_results(summary, output_file)

    print("\nMulti-step analysis test completed.")


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Debug the multi-step audio analysis process')
    parser.add_argument('--multi-step-analysis', metavar='FILE',
                        help='Run multi-step analysis on the specified audio file')

    args = parser.parse_args()

    if args.multi_step_analysis:
        test_multi_step_analysis(args.multi_step_analysis)
    else:
        # Test the multi-step analysis with the first available file
        test_multi_step_analysis()
