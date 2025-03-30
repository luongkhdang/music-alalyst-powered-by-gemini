#!/usr/bin/env python3
"""
run_app.py - Entry point for the MP3 to Image Generation Pipeline

Runs the main application from the project root to ensure imports work correctly.

Usage:
    python run_app.py --file FILENAME.mp3   # Process a single file
    python run_app.py --all                 # Process all MP3 files and clean output folders first
"""

import os
import sys
import argparse
import shutil
from pathlib import Path


def clean_output_folders():
    """Clean up all folders in the output directory"""
    output_dir = Path("output")
    if not output_dir.exists():
        return

    # Clean images folder
    images_dir = output_dir / "images"
    if images_dir.exists():
        # Remove all files in images directory
        for file_path in images_dir.glob("*.*"):
            if file_path.is_file():
                file_path.unlink()

        # Clean prompts subfolder
        prompts_dir = images_dir / "prompts"
        if prompts_dir.exists():
            for file_path in prompts_dir.glob("*.*"):
                if file_path.is_file():
                    file_path.unlink()

    print("Output folders cleaned successfully.")


# Run the main application
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="MP3 to Image Generation Pipeline")
    parser.add_argument(
        "--file", help="Process a single MP3 file from data_source folder")
    parser.add_argument("--all", action="store_true",
                        help="Process all MP3 files in data_source folder (cleans output folders first)")

    args = parser.parse_args()

    # Clean output folders if --all flag is used
    if args.all:
        clean_output_folders()

    # Import and run the main function from src/main.py
    from src.main import main
    main()
