"""
gemini_apis/file_api.py - File management API for Gemini

Provides functions for managing files with the Gemini API:
- list_files(client): Lists all files uploaded to Gemini
- delete_file(client, file_name): Deletes a file from Gemini
- upload_file(client, file_path): Uploads a file to Gemini

Related files:
- src/gemini/gemini_client.py: Main client that uses these API functions
- src/gemini/gemini_utilities/file_utils.py: Utility functions for file operations
"""

import logging
from typing import List, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def list_files(client) -> List[Any]:
    """
    List all files uploaded to Gemini.

    Args:
        client: Initialized Gemini client instance

    Returns:
        List of file objects
    """
    try:
        files = list(client.files.list())
        logger.info(f"Listed {len(files)} files")
        return files
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        return []


def delete_file(client, file_name: str) -> bool:
    """
    Delete a file from Gemini.

    Args:
        client: Initialized Gemini client instance
        file_name: Name of the file to delete

    Returns:
        True if successful, False otherwise
    """
    try:
        client.files.delete(name=file_name)
        logger.info(f"Deleted file: {file_name}")
        return True
    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}")
        return False


def upload_file(client, file_path: str) -> Any:
    """
    Upload a file to Gemini.

    Args:
        client: Initialized Gemini client instance
        file_path: Path to the file to upload

    Returns:
        File object reference
    """
    try:
        file = client.files.upload(file=file_path)
        logger.info(f"Uploaded file: {file_path}")
        return file
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise
