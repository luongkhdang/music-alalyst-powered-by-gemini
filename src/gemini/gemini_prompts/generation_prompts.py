"""
gemini_prompts/generation_prompts.py - Prompt templates for generation tasks

Provides prompt templates for various generation tasks:
- get_image_prompt_from_audio(): Returns a prompt for generating image prompts from audio
- get_image_generation_prompt(): Returns a prompt for generating an image from audio analysis
- get_story_generation_prompt(): Returns a prompt for generating stories
- get_creative_expansion_prompt(): Returns a prompt for expanding on a creative idea

Related files:
- src/gemini/gemini_client.py: Main client that uses these prompts
- src/gemini/gemini_hooks/audio_processor.py: Uses audio-to-image prompts
- src/gemini/gemini_hooks/image_processor.py: Uses image generation prompts
"""


def get_image_prompt_from_audio() -> str:
    """
    Get a prompt for generating an image prompt based on audio analysis.

    Returns:
        str: Prompt template for creating image prompts from audio analysis
    """
    return """
    Based on the audio analysis provided, create a detailed text prompt for generating 
    an image that captures the essence and vibe of this song. The prompt should be 
    descriptive, rich in visual details, and include:
    - A primary scene or subject
    - Color palette and mood
    - Lighting and atmosphere
    - Style (realistic, surreal, abstract, etc.)
    - Any unique visual elements that match the song's feeling
    
    Format your response as a JSON object with the following structure:
    {
        "prompt": "The complete image generation prompt (be detailed but concise)",
        "mood": "Primary mood of the song",
        "colors": ["list", "of", "dominant", "colors"],
        "style": "Suggested art style for the image"
    }
    """


def get_image_generation_prompt(analysis_text: str) -> str:
    """
    Generate a refined JSON prompt for an AI artist to create a visually compelling art splash 
    based on audio analysis, ideal for album covers, social media, or music videos.

    Args:
        analysis_text (str): Detailed analysis of the audio file capturing its technical, 
                             emotional, and visual essence.

    Returns:
        str: A JSON-formatted prompt translating the audio's core identity into a sophisticated 
             visual concept.
    """
    return f"""
    You are a visionary AI artist tasked with translating the soul of a musical track into a 
    striking visual masterpiece for album art, social media, or cinematic promotion. Your 
    expertise lies in distilling complex audio analyses into evocative, sophisticated imagery 
    that resonates with the track’s essence.

    Below is a detailed analysis of the track:
    ```
    {analysis_text}
    ```
    
    Using this analysis, craft a JSON prompt that encapsulates the track’s identity with 
    precision and artistry. Structure it as follows:

    {{
        "mood": "A concise, evocative 1-3 word phrase capturing the track’s emotional core",
        "colors": ["A curated palette of 3-5 colors reflecting the sonic and emotional tones"],
        "style": "A sophisticated artistic style aligning with the track’s character",
        "prompt": "A 50-100 word visual narrative for image generation, weaving mood, colors, 
                and key elements from the analysis (especially VISUAL ASSOCIATIONS) into a 
                cohesive, atmospheric scene or abstract composition suitable for high-impact 
                promotion"
    }}

    For the prompt:
    - Draw heavily from the VISUAL ASSOCIATIONS section, integrating scenes, imagery, and textures.
    - Weave in specific colors and mood to anchor the atmosphere.
    - Craft a unified scene or abstract form—avoid disjointed elements—balancing detail with 
    interpretive freedom.
    - Tailor the description for a polished, professional output ideal for album art or viral 
    social media splash.

    Return only the JSON object, formatted cleanly with proper indentation.
    """


def get_story_generation_prompt() -> str:
    """
    Get a prompt for story generation based on a theme or concept.

    Returns:
        str: Story generation prompt template
    """
    return """
    Create a compelling short story based on the theme/concept provided. Your story should:
    
    - Have a clear beginning, middle, and end
    - Include vivid descriptions and sensory details
    - Develop at least one main character with depth
    - Incorporate dialogue that feels natural and advances the plot
    - Build to a meaningful resolution or insight
    - Maintain a consistent tone that matches the theme
    
    Keep your story concise but complete, aiming for approximately 500-1000 words.
    Focus on quality of storytelling rather than length.
    
    Theme/Concept: [INPUT THEME HERE]
    """


def get_creative_expansion_prompt() -> str:
    """
    Get a prompt for creative expansion of ideas.

    Returns:
        str: Creative expansion prompt template
    """
    return """
    Take the following creative concept and expand it in multiple innovative directions.
    For each direction, provide:
    
    1. A clear framework or approach
    2. Key elements that would make this direction unique
    3. Potential challenges and how to address them
    4. Visual or emotional qualities to emphasize
    5. A sample implementation example
    
    Produce 3-5 distinct creative directions, each exploring different aspects of the
    original concept while maintaining its core essence.
    
    Original concept: [INPUT CONCEPT HERE]
    """
