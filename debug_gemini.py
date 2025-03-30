"""
Debug script to check Gemini module imports and implementations
"""

import os
import sys
import inspect

# Add src to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
print(f"Python path: {sys.path}")

# Try to import from src.gemini
print("\nImporting from src.gemini...")
try:
    import src.gemini.gemini_client as gemini_module
    print(f"Module file: {gemini_module.__file__}")

    from src.gemini.gemini_client import GeminiClient
    print(f"Successfully imported GeminiClient from src.gemini.gemini_client")

    # Check the module attributes
    print(f"Module attributes: {dir(gemini_module)}")

    # Create a client instance
    client = GeminiClient()
    print(f"GeminiClient instance created: {client}")

    # Check client attributes
    client_attributes = dir(client)
    print(f"Client attributes: {client_attributes}")

    # Check if our modular components exist
    if 'generator' in client_attributes:
        print("Client has generator attribute")
    else:
        print("Client does NOT have generator attribute")

    if 'analyzer' in client_attributes:
        print("Client has analyzer attribute")
    else:
        print("Client does NOT have analyzer attribute")

    if 'conversation' in client_attributes:
        print("Client has conversation attribute")
    else:
        print("Client does NOT have conversation attribute")

except Exception as e:
    print(f"Error importing from src.gemini: {e}")

# Try to clean __pycache__ directories
print("\nCleaning __pycache__ directories...")
for root, dirs, files in os.walk("src"):
    if "__pycache__" in dirs:
        pycache_dir = os.path.join(root, "__pycache__")
        print(f"Found: {pycache_dir}")
        for pyc_file in os.listdir(pycache_dir):
            if pyc_file.endswith(".pyc"):
                print(f"  Removing: {os.path.join(pycache_dir, pyc_file)}")
                try:
                    os.remove(os.path.join(pycache_dir, pyc_file))
                except Exception as e:
                    print(f"  Error removing: {e}")

# Try without the src prefix
print("\nImporting from gemini...")
try:
    from gemini.gemini_client import GeminiClient as OldGeminiClient
    print(f"Successfully imported GeminiClient from gemini.gemini_client")

    # Create a client
    old_client = OldGeminiClient()
    print(f"Old GeminiClient instance created: {old_client}")

    # Check if the old client has the modular components
    if hasattr(old_client, 'generator'):
        print("Old client has generator property")
    else:
        print("Old client does NOT have generator property")

except Exception as e:
    print(f"Error importing from gemini: {e}")
