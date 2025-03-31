"""
gemini_prompts/__init__.py - Prompt templates package for Gemini

Exports prompt templates for various tasks:
- Analysis prompts: For audio, image, and content analysis
- Generation prompts: For creating images, stories, and expanding ideas
- Multi-step analysis prompts: For the five-step viral music analysis
- Refinement prompts: For critical evaluation of final analysis

Related files:
- src/gemini/gemini_client.py: Main client that uses these prompts
- src/gemini/gemini_apis/: API functions that use these prompts
- src/gemini/gemini_hooks/: Hooks that use these prompts
"""

from src.gemini.gemini_prompts.analysis_prompts import (
    get_audio_analysis_prompt,
    get_image_analysis_prompt,
    get_content_analysis_prompt
)

from src.gemini.gemini_prompts.generation_prompts import (
    get_image_prompt_from_audio,
    get_story_generation_prompt,
    get_creative_expansion_prompt
)

from src.gemini.gemini_prompts.multi_step_analysis_prompts import (
    get_step1_prompt,
    get_step2_prompt,
    get_step3_prompt,
    get_step4_prompt,
    get_step5_prompt,
    get_final_integration_prompt
)

from src.gemini.gemini_prompts.refinement_prompt import (
    get_refinement_prompt,
    get_refinery_analyst1_prompt,
    get_refinery_analyst2_prompt,
    get_refinery_analyst3_prompt,
    get_refinery_analyst4_prompt,
    get_refinery_analyst5_prompt,
    get_final_refinery_prompt
)

__all__ = [
    # Analysis prompts
    'get_audio_analysis_prompt',
    'get_image_analysis_prompt',
    'get_content_analysis_prompt',

    # Generation prompts
    'get_image_prompt_from_audio',
    'get_story_generation_prompt',
    'get_creative_expansion_prompt',

    # Multi-step analysis prompts
    'get_step1_prompt',
    'get_step2_prompt',
    'get_step3_prompt',
    'get_step4_prompt',
    'get_step5_prompt',
    'get_final_integration_prompt',

    # Refinement prompts
    'get_refinement_prompt',
    'get_refinery_analyst1_prompt',
    'get_refinery_analyst2_prompt',
    'get_refinery_analyst3_prompt',
    'get_refinery_analyst4_prompt',
    'get_refinery_analyst5_prompt',
    'get_final_refinery_prompt'
]
