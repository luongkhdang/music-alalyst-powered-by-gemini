# Gemini-Discord Integration

A powerful integration that allows you to visualize and track Gemini API's responses in real-time using Discord webhooks.

## Features

- Send all Gemini API responses to Discord channels
- Track Gemini's "thinking process" for text generation, image analysis, and audio analysis
- Handle errors and send them to Discord for debugging
- Support for multimodal content analysis
- Maintain all the functionality of the original GeminiClient

## Requirements

- Python 3.7+
- Google Gemini API key
- Discord webhook URLs

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables in a `.env` file:

```
# Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Discord Webhooks
DISCORD_URL_WEBHOOK_ERRORS=https://discord.com/api/webhooks/your_error_webhook_url
DISCORD_URL_WEBHOOK_AI_ANALYSIS=https://discord.com/api/webhooks/your_analysis_webhook_url
DISCORD_URL_WEBHOOK_AI_MATERIALS=https://discord.com/api/webhooks/your_materials_webhook_url
DISCORD_CHARACTER_PER_MESSAGE_LIMIT=1900
```

## Usage

### Basic Usage

```python
from src.gemini.gemini_client import GeminiClient

# Initialize the client
client = GeminiClient()

# Generate text content
response = client.generate_content(
    "Explain how large language models like Gemini work in 3 paragraphs"
)

# The response will be sent to Discord automatically
print("Response sent to Discord successfully!")
```

### Analyzing Images

```python
# Analyze an image
image_path = "path/to/your/image.jpg"
response = client.analyze_image(
    image_path_or_file=image_path,
    prompt="Describe what you see in this image in detail."
)
```

### Analyzing Audio

```python
# Analyze an audio file
audio_path = "path/to/your/audio.mp3"
response = client.analyze_audio(
    audio_path_or_file=audio_path,
    prompt="Analyze this audio file and describe its characteristics."
)
```

### Chat Conversations

```python
# Create a chat session
client.create_chat(system_instruction="You are a helpful AI assistant.")

# Send messages in a conversation
response1 = client.send_message("Hello, can you help me with a question?")
response2 = client.send_message("What's the best way to learn Python?")

# All responses are automatically sent to Discord
```

### Multimodal Analysis

```python
from PIL import Image

# Load an image
image = Image.open("path/to/image.jpg")

# Create multimodal content (text + image)
contents = [
    "Analyze this image and tell me what you see.",
    image
]

# Analyze multimodal content
response = client.analyze_multimodal(contents)
```

## Discord Channel Setup

The integration uses three different Discord webhooks:

1. **Error Webhook**: For sending error messages and exceptions
2. **AI Analysis Webhook**: For final/complete analysis results
3. **AI Materials Webhook**: For intermediate results and "thinking process"

You can set these up in your Discord server by:

1. Go to Server Settings > Integrations > Webhooks
2. Create a new webhook for each channel
3. Copy the webhook URLs and add them to your `.env` file

## Examples

Check out the example scripts in the `src/examples` directory for more detailed usage patterns:

- `gemini_discord_example.py`: Full examples of various Gemini capabilities with Discord integration

## Advantages of Using This Integration

- **Real-time Visibility**: See exactly what Gemini is thinking and how it processes information
- **Debugging Support**: Easily identify and fix issues with your prompts or content
- **Collaborative Analysis**: Share AI outputs with your team via Discord channels
- **Comprehensive Logging**: Keep a record of all interactions with Gemini

## Notes on Gemini's Capabilities

Gemini is an advanced AI analyst capable of processing images, MP3 files, and text. It can generate both text and images as output. We can directly input MP3 and pictures to Gemini for analysis.

- **Input Context Window**: 1,048,576 tokens (very large)
- **Output Window**: 8,192 tokens
- **Best Practice**: Take advantage of the high input context window for every request, since the bottleneck is the output window
