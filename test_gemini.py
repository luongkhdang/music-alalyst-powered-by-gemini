#!/usr/bin/env python3
"""
Test script for verifying GeminiClient functionality
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    print("Trying to import GeminiClient...")
    from src.gemini.gemini_client import GeminiClient
    print("Import successful!")

    print("Initializing GeminiClient...")
    client = GeminiClient()
    print("Initialization successful!")

    print("All tests passed!")
except Exception as e:
    print(f"Error: {e}")
    print(f"Exception type: {type(e)}")
    print(f"Python path: {sys.path}")

    # Check if dotenv module is available
    try:
        import dotenv
        print("dotenv is available")
    except ImportError:
        print("dotenv is not available")

    # Check if PIL is available
    try:
        from PIL import Image
        print("PIL is available")
    except ImportError:
        print("PIL is not available")

    # Check if google.genai is available
    try:
        import google.genai
        print("google.genai is available")
    except ImportError:
        print("google.genai is not available")
