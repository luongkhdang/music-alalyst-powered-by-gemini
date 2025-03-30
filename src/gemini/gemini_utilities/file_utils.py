"""
gemini_utilities/file_utils.py - File handling utilities for the Gemini client

Provides utility functions for file operations:
- save_text(text, file_path): Saves text to a file
- save_json(data, file_path): Saves JSON data to a file
- save_image(image, file_path): Saves a PIL image to a file
- ensure_directory(directory): Ensures a directory exists
- clean_output_directory(directory): Cleans the content of a directory

Related files:
- src/gemini/gemini_client.py: Main client that uses these utilities
- src/gemini/gemini_apis/file_api.py: API functions for file operations
"""

import os
import json
import logging
import shutil
from pathlib import Path
from typing import Dict, Any, Union
from PIL import Image

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ensure_directory(directory: Union[str, Path]) -> None:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        directory: Directory path to ensure exists
    """
    directory_path = Path(directory)
    directory_path.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {directory}")


def save_text(text: str, file_path: Union[str, Path]) -> None:
    """
    Save text content to a file.

    Args:
        text: Text content to save
        file_path: Path where the file should be saved
    """
    try:
        # Ensure parent directory exists
        ensure_directory(Path(file_path).parent)

        # Write the text file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        logger.info(f"Saved text file: {file_path}")
    except Exception as e:
        logger.error(f"Error saving text file {file_path}: {e}")
        raise


def save_json(data: Dict[str, Any], file_path: Union[str, Path]) -> None:
    """
    Save data as a JSON file.

    Args:
        data: Dictionary data to save as JSON
        file_path: Path where the file should be saved
    """
    try:
        # Ensure parent directory exists
        ensure_directory(Path(file_path).parent)

        # Write the JSON file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved JSON file: {file_path}")
    except Exception as e:
        logger.error(f"Error saving JSON file {file_path}: {e}")
        raise


def save_image(image: Image.Image, file_path: Union[str, Path]) -> None:
    """
    Save a PIL image to a file.

    Args:
        image: PIL Image object to save
        file_path: Path where the image should be saved
    """
    try:
        # Ensure parent directory exists
        ensure_directory(Path(file_path).parent)

        # Save the image
        image.save(file_path)
        logger.info(f"Saved image: {file_path}")
    except Exception as e:
        logger.error(f"Error saving image {file_path}: {e}")
        raise


def clean_output_directory(directory: Union[str, Path]) -> bool:
    """
    Clean the contents of a directory without deleting the directory itself.

    Args:
        directory: Directory to clean

    Returns:
        bool: True if cleaning was successful
    """
    try:
        directory_path = Path(directory)

        # Check if directory exists
        if not directory_path.exists():
            logger.info(f"Directory does not exist, creating: {directory}")
            directory_path.mkdir(parents=True, exist_ok=True)
            return True

        # Delete contents
        for item in directory_path.glob('*'):
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

        logger.info(f"Cleaned directory: {directory}")
        return True
    except Exception as e:
        logger.error(f"Error cleaning directory {directory}: {e}")
        return False
