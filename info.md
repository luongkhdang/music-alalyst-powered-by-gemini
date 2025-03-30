# System Instructions and Configuration Guide for Gemini SDK

## System Instructions

System instructions allow you to customize a model's behavior for your specific use case. By providing system instructions, you give the model additional context to tailor its responses, ensuring it adheres to your defined behavior throughout the user interaction. This separates product-level configuration from end-user prompts.

You can set system instructions when initializing your model. Here’s an example:

### Python Example

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="GEMINI_API_KEY")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a cat. Your name is Neko."
    ),
    contents="Hello there"
)

print(response.text)
```

The model will then respond as "Neko the cat" for the entire session.

---

## Configuration Parameters

Every prompt sent to the model includes parameters that control response generation. You can customize these parameters or rely on default settings.

### Example Configuration

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="GEMINI_API_KEY")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["Explain how AI works"],
    config=types.GenerateContentConfig(
        max_output_tokens=500,
        temperature=0.1
    )
)

print(response.text)
```

### Configurable Parameters

- **stopSequences**: A list of up to 5 character sequences that halt generation. The API stops at the first occurrence, excluding the sequence from the response.
- **temperature**: Controls randomness. Range: `[0.0, 2.0]`. Higher values (e.g., `1.0`) yield creative outputs; lower values (e.g., `0.1`) produce deterministic responses.
- **maxOutputTokens**: Limits the response length in tokens.
- **topP**: Filters tokens by cumulative probability (default: `0.95`). Tokens are selected until their probabilities sum to this value.
- **topK**: Limits token selection to the `k` most probable options, further refined by `topP` and sampled using `temperature`.

> **Note:** Parameter names may vary slightly by programming language.

---

## Multi-Turn Conversations

The Gemini SDK supports multi-turn chats, enabling users to build on previous questions and responses. The chat interface tracks conversation history while internally using `generateContent` to produce responses.

### Basic Chat Example

```python
from google import genai

client = genai.Client(api_key="GEMINI_API_KEY")
chat = client.chats.create(model="gemini-2.0-flash")

response = chat.send_message("I have 2 dogs in my house.")
print(response.text)

response = chat.send_message("How many paws are in my house?")
print(response.text)

# Display conversation history
for message in chat.get_history():
    print(f"role - {message.role}: {message.parts[0].text}")
```

### Streaming Chat Example

```python
from google import genai

client = genai.Client(api_key="GEMINI_API_KEY")
chat = client.chats.create(model="gemini-2.0-flash")

response = chat.send_message_stream("I have 2 dogs in my house.")
for chunk in response:
    print(chunk.text, end="")

response = chat.send_message_stream("How many paws are in my house?")
for chunk in response:
    print(chunk.text, end="")

# Display conversation history
for message in chat.get_history():
    print(f"role - {message.role}: {message.parts[0].text}")
```

---

## Working with Audio Files

You can provide audio files to Gemini in two ways:

1. Upload the file using the **File API** (recommended for files >20 MB).
2. Inline data within the prompt request.

### Upload an Audio File and Generate Content

The **File API** supports uploads up to **2 GB per file**, with a **20 GB project limit**. Files are stored for **48 hours** and accessible with your API key (no downloads).

#### Example

```python
from google import genai

client = genai.Client()

myfile = client.files.upload(file="media/sample.mp3")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["Describe this audio clip", myfile]
)

print(response.text)
```

### Get File Metadata

Verify an upload and retrieve metadata:

```python
myfile = client.files.upload(file="media/sample.mp3")
file_name = myfile.name
myfile = client.files.get(name=file_name)
print(myfile)
```

### List Uploaded Files

```python
print("My files:")
for f in client.files.list():
    print(f" {f.name}")
```

### Delete Uploaded Files

Files auto-delete after **48 hours**, but you can manually remove them:

```python
myfile = client.files.upload(file="media/sample.mp3")
client.files.delete(name=myfile.name)
```

---

## Image Input

The **Gemini API** supports multimodal inputs, combining text and media like images. You can generate text based on both text and image inputs.

### Example: Text and Image Input

```python
from PIL import Image
from google import genai

client = genai.Client(api_key="GEMINI_API_KEY")

image = Image.open("/path/to/organ.png")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[image, "Tell me about this instrument"]
)

print(response.text)
```

---

## Generate Images

The **Gemini API** supports image generation using models like `gemini-2.0-flash-exp-image-generation` (Gemini 2.0 Flash Experimental) and **Imagen 3**. This section focuses on **Gemini 2.0**, which can generate text and inline images conversationally. Generated images include a **SynthID watermark**, with visible watermarks added in **Google AI Studio**.

> **Note:** For text-and-image output, set `response_modalities=["Text", "Image"]` in the configuration. Image-only output is not supported.

### Example: Generate Text and Image

```python
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

client = genai.Client(api_key="GEMINI_API_KEY")

contents = (
    "Hi, can you create a 3D rendered image of a pig with wings and a top hat "
    "flying over a happy futuristic sci-fi city with lots of greenery?"
)

response = client.models.generate_content(
    model="gemini-2.0-flash-exp-image-generation",
    contents=contents,
    config=types.GenerateContentConfig(
        response_modalities=["Text", "Image"]
    )
)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.save("gemini-native-image.png")
        image.show()
```

---

This guide provides a **clear, developer-friendly** overview of system instructions, configuration options, multi-turn chats, and audio file handling with the **Gemini SDK**. Let me know if you'd like further refinements!
