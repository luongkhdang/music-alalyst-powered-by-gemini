"""
gemini_prompts/analysis_prompts.py - Prompt templates for analysis tasks

Provides prompt templates for various analysis tasks:
- get_audio_analysis_prompt(): Returns a detailed prompt for audio analysis
- get_image_analysis_prompt(): Returns a prompt for image analysis
- get_content_analysis_prompt(): Returns a general content analysis prompt

Related files:
- src/gemini/gemini_client.py: Main client that uses these prompts
- src/gemini/gemini_apis/audio_api.py: Uses audio analysis prompts
- src/gemini/gemini_apis/image_api.py: Uses image analysis prompts
"""


def get_audio_analysis_prompt() -> str:
    """
    Get a comprehensive prompt for audio analysis.

    Returns:
        str: Detailed prompt for analyzing audio files
    """
    return """
    Analyze this audio file in comprehensive detail. Please cover:
    
    1. TECHNICAL ASPECTS:
       - Genre classification and sub-genres
       - Tempo (BPM) and rhythm patterns
       - Key signature and chord progressions
       - Production quality and techniques
       - Instrument identification
       
    2. EMOTIONAL QUALITIES:
       - Overall mood and atmosphere
       - Emotional journey throughout the track
       - Intensity curves and dynamic range
       - Psychological impact on listeners
       
    3. VISUAL ASSOCIATIONS:
       - Color palette that represents the sound
       - Visual scenes or imagery evoked
       - Textures and physical sensations suggested
       - Environmental settings that match the audio
       
    4. CREATIVE DIRECTION:
       - Artistic intentions behind production choices
       - Cultural or historical references
       - Innovative or unique elements
       - Potential use cases (film, advertising, etc.)
       
    Provide substantive detail in each section. This analysis will be used to guide visual art generation.
    """


def get_image_analysis_prompt() -> str:
    """
    Get a prompt for comprehensive image analysis.

    Returns:
        str: Detailed prompt for analyzing images
    """
    return """
    Analyze this image in comprehensive detail. Please cover:
    
    1. VISUAL COMPOSITION:
       - Subject matter and focal points
       - Color palette and color relationships
       - Composition, layout, and framing
       - Style and artistic technique
       - Lighting and atmosphere
       
    2. EMOTIONAL IMPACT:
       - Overall mood and feeling
       - Emotional response it evokes
       - Symbolic or metaphorical elements
       - Narrative or story suggested
       
    3. TECHNICAL QUALITY:
       - Level of detail and clarity
       - Execution quality
       - Special techniques or effects used
       - Digital vs. traditional medium characteristics
       
    4. CONTEXTUAL CONSIDERATIONS:
       - Potential purpose or use case
       - Cultural references or influences
       - Target audience
       - Contemporary vs. historical style elements
       
    Provide substantive detail in each section, being as specific and descriptive as possible.
    """


def get_content_analysis_prompt() -> str:
    """
    Get a general prompt for analyzing text content.

    Returns:
        str: General content analysis prompt
    """
    return """
    Analyze this content thoroughly and provide a detailed breakdown covering:
    
    1. MAIN THEMES AND IDEAS:
       - Primary subject matter
       - Key arguments or positions
       - Underlying themes or messages
       
    2. STRUCTURE AND STYLE:
       - Organization and flow
       - Tone and voice
       - Stylistic choices and rhetorical devices
       
    3. CONTEXT AND RELEVANCE:
       - Historical or cultural context
       - Current relevance
       - Target audience considerations
       
    4. CRITICAL ASSESSMENT:
       - Strengths and effective elements
       - Potential weaknesses or limitations
       - Suggestions for improvement or expansion
       
    Provide a balanced analysis with specific examples from the content to support your observations.
    """
