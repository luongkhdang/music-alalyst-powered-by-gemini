# Gemini Client with Discord Integration

A unified Python client for interacting with Google's Gemini API and Discord, supporting:

- Text generation with context window of 1,048,576 tokens
- Multi-turn conversations
- Audio file processing (MP3)
- Image input and analysis
- Image generation
- Discord integration for real-time response tracking
- Output generation up to 8,192 tokens
- Error handling with Discord notifications

## Installation

```bash
pip install -r requirements.txt
```

## Setup

You'll need to set up your Gemini API key and Discord webhook URLs. You can either:

1. Set them as environment variables:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```
2. Or pass the API key directly when initializing the client

You can also configure the following in your `.env` file:

```
GEMINI_API_KEY=your-api-key
DISCORD_WEBHOOK_ANALYSIS=your-discord-webhook-url
DISCORD_WEBHOOK_MATERIALS=your-discord-webhook-url
DISCORD_WEBHOOK_ERRORS=your-discord-webhook-url
```

## Usage Examples

### Basic Text Generation with Discord Integration

```python
from src.gemini.gemini_client import GeminiClient

# Initialize the client
client = GeminiClient(api_key="your-api-key")  # or use environment variable

# Generate content and automatically send to Discord
response = client.generate_content("Explain quantum computing in simple terms")
print(response)
```

### Chat Conversation

```python
from src.gemini.gemini_client import GeminiClient

client = GeminiClient()

# Create a chat session
client.create_chat(system_instruction="You are a helpful assistant")

# Send messages - responses are automatically sent to Discord
response = client.send_message("What's the weather like today?")
print(response)

# Follow-up question with temperature adjustment
response = client.send_message("How about tomorrow?", temperature=0.8)
print(response)

# Get chat history
history = client.get_chat_history()
for message in history:
    print(f"{message['role']}: {message['text']}")
```

### Image Analysis

```python
from src.gemini.gemini_client import GeminiClient
from PIL import Image

client = GeminiClient()

# Analyze an image from file path
analysis = client.analyze_image("path/to/image.jpg",
                              "What objects can you see in this image?")
print(analysis)

# Or analyze from a PIL Image object
image = Image.open("path/to/image.jpg")
analysis = client.analyze_image(image, "Describe this image in detail")
print(analysis)
```

### Audio Analysis

```python
from src.gemini.gemini_client import GeminiClient

client = GeminiClient()

# Analyze an audio file
analysis = client.analyze_audio("path/to/audio.mp3",
                              "Analyze the mood, genre, and key elements of this music")
print(analysis)
```

### Image Generation

```python
from src.gemini.gemini_client import GeminiClient

client = GeminiClient()

# Generate an image
description, image = client.generate_image(
    "A surrealistic landscape with floating islands and waterfalls, in the style of Salvador Dali"
)

# Save the generated image
image.save("generated_image.png")
print(f"Image description: {description}")
```

### Error Handling

All methods include automatic error handling that will send errors to your configured Discord error webhook.

## Working with Files

```python
from gemini.gemini_client import GeminiClient

client = GeminiClient()

# Upload a file
uploaded_file = client.upload_file("path/to/file.mp3")

# List uploaded files
files = client.list_files()
for file in files:
    print(f"Name: {file['name']}, Type: {file['mime_type']}")

# Delete a file when done
client.delete_file(uploaded_file.name)
```

## Streaming Responses

For lengthy responses, streaming can provide a better user experience:

```python
from gemini.gemini_client import GeminiClient

client = GeminiClient()

# Stream content
for chunk in client.stream_content("Write a 500 word essay about climate change"):
    print(chunk, end="", flush=True)

# Stream in chat
client.create_chat()
for chunk in client.stream_message("Tell me a story about a brave knight"):
    print(chunk, end="", flush=True)
```

## Rate Limiting

The client includes built-in rate limiting to prevent exceeding API quotas:

```python
from gemini.gemini_client import GeminiClient

client = GeminiClient()

# Check remaining API calls
remaining = client.get_rate_limit_status()
print(f"Remaining calls this minute: {remaining['minute']}")
print(f"Remaining calls today: {remaining['day']}")

# Make API calls without worrying about rate limits
# The client will automatically wait if necessary
for i in range(20):
    response = client.generate_content(f"Generate idea #{i}")
    print(response)
```
