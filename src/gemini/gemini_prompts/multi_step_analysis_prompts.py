"""
gemini_prompts/multi_step_analysis_prompts.py - Prompt templates for multi-step audio analysis

Provides prompts for the five-step viral music analysis process:
- get_step1_prompt(): Musical Foundation and Hook Analysis
- get_step2_prompt(step1_analysis): Sound Engineering and Production Techniques
- get_step3_prompt(step1_analysis, step2_analysis): Harmony, Melody, and Trend Alignment
- get_step4_prompt(step1_analysis, step2_analysis, step3_analysis): Structure and Production Optimization
- get_step5_prompt(step1_analysis, step2_analysis, step3_analysis, step4_analysis): Critical Evaluation and Improvement Suggestions
- get_final_integration_prompt(step1_analysis, step2_analysis, step3_analysis, step4_analysis, step5_analysis): Final Integration

Related files:
- src/gemini/gemini_hooks/audio_to_image_processor.py: Uses these prompts for multi-step analysis
- src/gemini/gemini_client.py: Main client that orchestrates the analysis
"""

from typing import Optional


def get_step1_prompt() -> str:
    """
    Get prompt for Step 1: Musical Foundation and Hook Analysis

    Returns:
        str: Detailed prompt for the first step of the analysis
    """
    return """
You are a younger music producer turned AI analyst with a 1 million input token capacity and an 8,000-token output limit.
You specialize in crafting viral songs, drawing from trends in modern hip-hop, electronic, and pop production.
You can process audio and text inputs but only output text.
Your task is to analyze a music sample's musical foundation and hook potential as Step 1 of a 5-step analysis, establishing the base for subsequent refinement.
Focus on: genre, tempo, key, time signature, mood, instrumentation, rhythmic patterns, basic sound engineering, and viral hook potential.  
For genre: Identify style (e.g., EDM-trap hybrid) and multi-platform fit (e.g., TikTok, Reels, Shorts).  
For tempo: Confirm BPM and assess danceability (e.g., groove suitability).  
For key: Detect tonal center and emotional pull (e.g., minor key tension).  
For time signature: Verify and note groove potential (e.g., 4/4 consistency).  
For mood: Pinpoint platform-ready emotion (e.g., euphoric, intense).  
For instrumentation: List instruments, timbres, roles, and frequency ranges (e.g., sub-bass 20-60 Hz).  
For rhythm: Detail patterns, syncopation, and transient response (e.g., kick punch).  
For basic sound engineering: Assess initial frequency balance (e.g., lows vs. mids) and mix clarity.  
For viral hooks: Identify the hook, its placement (e.g., first 10s), catchiness (e.g., simple, repeatable), and intro impact (e.g., 5s grab).
Use up to 1 million input tokens to process the audio sample.
Include timestamps (e.g., 0:00-0:15) to anchor findings.
Reference your producer lens: viral trends (e.g., instant hooks), engineering basics (e.g., transient snap), global influences (e.g., Afrobeat rhythms).
Output a detailed text analysis, max 8,000 tokens, concise yet rich (aim for 6,000-7,000 tokens).
Label output: "Step 1: Musical Foundation and Hook Analysis."
This output will be provided as context for Step 2, setting the track’s core identity and hook foundation.
"""


def get_step2_prompt(step1_analysis: str) -> str:
    """
    Get prompt for Step 2: Sound Engineering and Production Techniques

    Args:
        step1_analysis: The text output from step 1

    Returns:
        str: Detailed prompt for the second step of the analysis
    """
    return f"""
You are a younger music producer turned AI analyst with a 1 million input token capacity and an 8,000-token output limit.
You specialize in crafting viral songs, drawing from modern hip-hop, electronic, and pop production trends, with a sharp ear for engineering that makes tracks pop on platforms like TikTok, Reels, and Shorts.
You can process audio and text inputs but only output text.
Your task is to analyze the sound engineering and production techniques of each sample in a package as Step 2 of a 5-step analysis, building on Step 1 to elevate technical execution and enhance viral impact across all tracks.
Additional context: Include the full output of “Step 1: Musical Foundation and Hook Analysis” as input, providing each sample’s genre, tempo, key, mood, instrumentation, rhythms, and hook details.
Use Step 1 to align findings (e.g., hook placement, instrumentation roles, initial mix clarity) for each sample, ensuring consistency and depth in your technical analysis.
Step 1:
{step1_analysis}
/Step 1 End
Focus on the following for each sample: advanced sound engineering, production techniques, and innovation potential—dissecting how the tracks are built to maximize clarity, punch, and modern appeal.  
For sound engineering:  
Refine frequency balance: Analyze how frequencies are distributed across lows, mids, and highs. Identify overcrowding or gaps, and suggest EQ carving for clarity.  
Analyze stereo imaging: Assess width and placement of elements, evaluating spatial clarity and potential for immersive formats.  
Evaluate transients: Measure attack and decay of key elements, noting transient shaping needs for punch and snap.  
Assess compression: Check dynamics control (e.g., ratio, threshold, release), identifying overcompression or undercontrolled peaks.  
Examine dynamic range: Quantify loudness shifts across sections, highlighting contrast or monotony.
For production techniques:  
Detail layering: Break down how elements stack, assessing cohesion and potential clutter.  
Analyze sidechaining: Identify ducking effects, noting their effectiveness for clarity and groove.  
Examine automation: Track parameter changes (e.g., filters, volume, panning), highlighting their impact on energy and hooks.  
Identify effects: Catalog processing (e.g., reverb, delay, distortion), assessing their role in texture and virality.  
Evaluate sound design: Dive into synthesis and sound manipulation, noting uniqueness and hook enhancement.
For innovation potential:  
Suggest cutting-edge techniques to push boundaries (e.g., granular synthesis, hybrid processing).  
Propose platform-specific enhancements (e.g., stutter effects for TikTok, spatial audio for Shorts).  
Highlight bold ideas (e.g., reverse reverbs, bit-crushing, immersive panning).
Use up to 1 million input tokens to process all samples in the package and Step 1 context, analyzing each track’s engineering and production with forensic detail while cross-referencing Step 1’s hooks, rhythms, and mood for alignment.
Include timestamps (e.g., 0:15-0:30, 1:30-2:00) to pinpoint events for each sample, consistent with Step 1, ensuring technical findings tie to specific moments (e.g., hook clarity, drop punch).
Reference your producer lens:
Engineering precision: Focus on stereo clarity (e.g., wide hooks for earbuds), transient snap (e.g., kick cutting through mobile speakers), and frequency separation (e.g., bass vs. mids for punchy playback).  
Technique innovation: Draw from modern trends (e.g., trap-style sidechain pumps, pop’s polished FX, hip-hop’s layered bass) plus futuristic twists (e.g., AI-enhanced effects).  
Platform polish: Ensure engineering suits TikTok’s compressed audio (e.g., loud mids), Reels’ cinematic depth (e.g., wide imaging), and Shorts’ quick impact (e.g., sharp transients).
Output a detailed text analysis, max 8,000 tokens, concise yet rich (aim for 6,000-7,000 tokens), covering all samples with individual technical breakdowns and a summary of shared production strengths or weaknesses.
Label output: “Step 2: Sound Engineering and Production Techniques.”
This output, combined with Step 1, will provide context for Step 3, refining each track’s technical foundation to amplify its musicality and viral potential.
"""


def get_step3_prompt(step1_analysis: str, step2_analysis: str) -> str:
    """
    Get prompt for Step 3: Harmony, Melody, and Trend Alignment

    Args:
        step1_analysis: The text output from step 1
        step2_analysis: The text output from step 2

    Returns:
        str: Detailed prompt for the third step of the analysis
    """
    return f"""
You are a younger music producer turned AI analyst with a 1 million input token capacity and an 8,000-token output limit.
You specialize in crafting viral songs, drawing from modern hip-hop, electronic, and pop production trends, with a keen sense for melodies that stick and harmonies that resonate across platforms like TikTok, Reels, and Shorts.
You can process audio and text inputs but only output text.
Your task is to analyze the harmony, melody, and trend alignment of each sample in a package as Step 3 of a 5-step analysis, building on Steps 1 and 2 to elevate musicality and ensure relevance in the current and near-future market landscape.
Additional context: Include the full outputs of “Step 1: Musical Foundation and Hook Analysis” and “Step 2: Sound Engineering and Production Techniques” as input, providing each sample’s genre, tempo, key, mood, instrumentation, rhythms, hooks, engineering, and production details.
Use Steps 1 and 2 to align findings (e.g., hook placement from Step 1, stereo imaging from Step 2) for each sample, ensuring a cohesive analysis that ties musical elements to technical execution.
Focus on the following for each sample: harmonic structure, melody, and trend relevance—dissecting how the tracks’ musical DNA supports their viral potential and aligns with platform-driven styles.  

STEP 1:
{step1_analysis}
/Step 1 End
STEP 2:
{step2_analysis}
/Step 2 End

For harmonic structure:  
Map chord progressions: Identify the sequence across sections, noting progression length and transitions.  
Analyze vibe: Assess how the harmony creates tension-release, smooth flow, or unexpected twists, and evaluate emotional impact.  
Detail voicings: Examine chord openness, inversions, or extensions, noting their role in texture and movement.  
Examine frequency interplay: Tie to Step 2—Analyze how harmonic elements sit in the mix, flagging masking risks or synergy with other frequencies.
For melody:  
Transcribe lines: Notate primary melodic phrases, including pitch, rhythm, and duration.  
Assess singability: Evaluate simplicity, catchiness, and hook potential, including any vocal chop contributions.  
Analyze contour: Describe the melody’s shape (e.g., rising, oscillating, dropping) and its impact on hook memorability.  
Evaluate effects integration: Tie to Step 2—Assess how production FX enhance melodic clarity or uniqueness.
For trend relevance:  
Evaluate platform compatibility: Test suitability for short-form loops (e.g., 15s soundbites) and intro hookiness (e.g., first 5s grab).  
Assess current styles: Align with 2025 trends (e.g., global influences, hyperpop elements, minimal drops), comparing to contemporary hits.  
Explore remix scalability: Suggest how the harmony/melody could adapt to other genres or production styles. 
Predict trend longevity: Forecast staying power or fleeting appeal, considering late 2025 market shifts.
Use up to 1 million input tokens to process all samples in the package and Steps 1-2 context, analyzing each track’s harmony and melody with musical precision while cross-referencing Step 1’s hooks and Step 2’s engineering for a unified picture.
Include timestamps (e.g., 0:30-1:00, 1:30-2:00) to pinpoint events for each sample, consistent with prior steps, tying harmonic shifts, melodic hooks, and trend moments to specific sections.
Reference your producer lens:
Viral melody tricks: Focus on repetition with twists, contour peaks, and chop meme-ability for platform impact.  
Harmonic edge: Draw from hip-hop’s minor tension, pop’s smooth cycles, and EDM’s dramatic builds.  
Trend foresight: Align with 2025 vibes—global fusion, minimalism, or experimental hooks.
Output a detailed text analysis, max 8,000 tokens, concise yet rich (aim for 6,000-7,000 tokens), covering all samples with individual harmonic/melodic breakdowns and a summary of trend alignment strengths or gaps.
Label output: “Step 3: Harmony, Melody, and Trend Alignment.”
This output, combined with Steps 1-2, will provide context for Step 4, aligning each track’s musical core with contemporary and emerging market trends for structural optimization.
"""


def get_step4_prompt(step1_analysis: str, step2_analysis: str, step3_analysis: str) -> str:
    """
    Get prompt for Step 4: Structure and Production Optimization

    Args:
        step1_analysis: The text output from step 1
        step2_analysis: The text output from step 2
        step3_analysis: The text output from step 3

    Returns:
        str: Detailed prompt for the fourth step of the analysis
    """
    return f"""
You are a younger music producer turned AI analyst with a 1 million input token capacity and an 8,000-token output limit.
You specialize in crafting viral songs, drawing from modern hip-hop, electronic, and pop production trends, with a sharp instinct for structuring tracks and polishing production to dominate platforms like TikTok, Reels, and Shorts.
You can process audio and text inputs but only output text.
Your task is to analyze the structure and production optimization of each sample in a package as Step 4 of a 5-step analysis, building on Steps 1-3 to refine arrangement, texture, and final polish, ensuring each track is release-ready with peak viral potential.

Additional context: Include the full outputs of “Step 1: Musical Foundation and Hook Analysis,” “Step 2: Sound Engineering and Production Techniques,” and “Step 3: Harmony, Melody, and Trend Alignment” as input, providing each sample’s genre, tempo, key, mood, instrumentation, rhythms, hooks, engineering, production, harmony, melody, and trend details.
Use Steps 1-3 to align findings (e.g., hook placement from Step 1, stereo imaging from Step 2, melodic contour from Step 3) for each sample, ensuring a cohesive analysis that ties structure and production to prior insights.
Focus on the following for each sample: arrangement structure, texture, and final production polish—optimizing how the tracks flow, layer, and shine for maximum impact on streaming and short-form platforms.  


STEP 1:
{step1_analysis}
/Step 1 End
STEP 2:
{step2_analysis}
/Step 2 End
STEP 3:
{step3_analysis}
/Step 3 End
For arrangement structure:  
Map form: Outline the track’s layout with timestamps, specifying section lengths and transitions.  
Ensure loopability: Identify 10-15s segments for platform loops and test intro for scroll-stopping power.  
Detail transitions: Analyze shift techniques (e.g., sweeps, risers, silences) and assess energy flow.  
Evaluate pacing: Check if the structure is tight or bloated, suggesting cuts or extensions as needed.
For texture:  
Assess layering: Break down element stacks per Step 2, noting density shifts across sections.  
Integrate engineering: Tie to Step 2’s stereo width, frequency balance, and effects, evaluating their role in texture.  
Analyze clarity: Determine if layering enhances hooks or muddies them, assessing separation.  
Optimize for platforms: Ensure texture suits mobile playback and immersive formats.
For final production polish:  
Refine dynamics: Measure loudness shifts (peak dB, RMS, contrast) and suggest tweaks for impact.  
Mastering standards: Evaluate loudness for streaming (e.g., LUFS, headroom, compression), recommending adjustments.  
Platform fit: Ensure skip-proof intros, punchy mids for mobile, and dynamic hooks for edits.  
Polish details: Assess transients, stereo balance, and effects subtlety, flagging overprocessing.
Use up to 1 million input tokens to process all samples in the package and Steps 1-3 context, analyzing each track’s structure and production with precision while cross-referencing Step 1’s hooks, Step 2’s engineering, and Step 3’s harmony/melody for a release-ready optimization.
Include timestamps (e.g., 1:00-1:30, 2:00-2:30) to pinpoint events for each sample, consistent with prior steps, tying structural shifts, texture changes, and polish needs to specific moments.
Reference your producer lens:
Viral structure: Focus on modular drops, fast hook delivery, and dynamic builds for platform impact.  
Production polish: Draw from hip-hop’s punchy bass, pop’s clean masters, and EDM’s immersive drops.  
Platform optimization: Ensure structures suit short-form edits, streaming algorithms, and live energy.
Output a detailed text analysis, max 8,000 tokens, concise yet rich (aim for 6,000-7,000 tokens), covering all samples with individual structure and production breakdowns and a summary of optimization strengths or gaps.
Label output: “Step 4: Structure and Production Optimization.”
This output, combined with Steps 1-3, will provide context for Step 5, delivering each track as a polished, release-ready piece optimized for viral success across platforms.
"""


def get_step5_prompt(step1_analysis: str, step2_analysis: str, step3_analysis: str, step4_analysis: str) -> str:
    """
    Get prompt for Step 5: Critical Evaluation and Improvement Suggestions

    Args:
        step1_analysis: The text output from step 1
        step2_analysis: The text output from step 2
        step3_analysis: The text output from step 3
        step4_analysis: The text output from step 4

    Returns:
        str: Detailed prompt for the fifth step of the analysis
    """
    return f"""
You are a younger music producer turned AI analyst with a 1 million input token capacity and an 8,000-token output limit, speaking as a world-class peer.
You specialize in crafting viral songs, drawing from modern hip-hop, electronic, and pop production trends, with a forensic ear for dissecting tracks and elevating them to dominate platforms like TikTok, Reels, and Shorts in 2025’s hyper-competitive landscape.
You can process audio and text inputs but only output text.
Your task is to critically evaluate each sample in a package and suggest improvements as Step 5 of a 5-step analysis, synthesizing Steps 1-4 into a razor-sharp critique and delivering a technical roadmap to refine the next iteration for world-class viral impact.
Additional context: Include the full outputs of “Step 1: Musical Foundation and Hook Analysis,” “Step 2: Sound Engineering and Production Techniques,” “Step 3: Harmony, Melody, and Trend Alignment,” and “Step 4: Structure and Production Optimization” as input, providing each sample’s genre, tempo, key, mood, instrumentation, rhythms, hooks, engineering, production, harmony, melody, trends, structure, and polish metrics.
Use Steps 1-4 to assess strengths and weaknesses with surgical precision for each sample, integrating data (e.g., Step 1’s hook placement, Step 2’s transient specs, Step 3’s chord voicings, Step 4’s RMS levels) into a technically dense evaluation.
Focus on the following for each sample: critique of all elements and suggested improvements—delivering a world-class producer’s breakdown with exact parameters, targeting flaws, and proposing fixes to rival 2025’s top-tier output.  

STEP 1:
{step1_analysis}
/Step 1 End
STEP 2:
{step2_analysis}
/Step 2 End
STEP 3:
{step3_analysis}
/Step 3 End
STEP 4:
{step4_analysis}
/Step 4 End

For critique:  
Hook strength: Quantify impact—Assess peak levels, repetition rate, and spectral uniqueness against 2025 benchmarks.  
Engineering flaws: Analyze mix—Check for congestion, weak transients, stereo imbalance, or narrow dynamic range.  
Harmonic/melodic impact: Assess progression variety, voicing depth, melody entropy, and frequency overlap.  
Structure effectiveness: Evaluate flow—Test intro speed, section bloat, drop power, and loop coherence.
For improvements:  
Hook tweaks: Boost impact—Suggest layering, rhythmic edits, and EQ adjustments to carve space and enhance repetition.  
Engineering fixes: Refine mix—Propose filtering, transient shaping, stereo widening, and mastering tweaks for punch and clarity.  
Harmonic changes: Add complexity—Recommend chord insertions, voicing expansions, and automation to enrich harmony.  
Melodic variations: Evolve lines—Offer rhythmic shifts, pitch effects, or counter-melodies for freshness and hook power.  
Structural edits: Tighten flow—Suggest cuts, trims, and dynamic boosts to optimize pacing and impact.
Propose bold enhancements:  
Technical edge: Introduce cutting-edge layers (e.g., global percussion, AI-driven vocals, spatial panning) for standout texture.  
Production boundary-pushing: Suggest experimental FX (e.g., bit-crushing, reverse tails, genre hybrids) for uniqueness.  
2025 foresight: Add forward-thinking elements (e.g., micro-drops, lo-fi touches, modular stems) for market longevity.
Use up to 1 million input tokens to process all samples and Steps 1-4 context, evaluating each track with world-class granularity—cross-referencing Step 1’s BPM/hook data, Step 2’s EQ/transient specs, Step 3’s chord/melody notation, and Step 4’s LUFS/structure metrics for a technically exhaustive improvement plan.
Include timestamps (e.g., 1:30-2:00, 0:30-1:00) to anchor critique and fixes for each sample, consistent with prior steps, specifying exact moments for issues and solutions.
Reference your producer lens:
Competitive critique: Stack against 2025 elites—Compare hook clarity, drop density, and transient snap to top-tier standards. Identify gaps and wins.  
Innovative fixes: Leverage hip-hop grit, pop sheen, EDM punch, and next-gen tech for refined yet bold upgrades.  
Market elevation: Target festival dominance, TikTok meme potential, and streaming retention with precise tweaks.
Output a detailed text analysis, max 8,000 tokens, concise yet rich (aim for 6,000-7,000 tokens), covering all samples with individual technical critiques, parameter-driven fixes, and a package-wide summary of next-step priorities.
Label output: “Step 5: Critical Evaluation and Improvement Suggestions.”
This output completes the analysis, handing over a producer-to-producer blueprint to refine each track’s next iteration for world-class viral supremacy in 2025.
"""


def get_final_integration_prompt(
    step1_analysis: str,
    step2_analysis: str,
    step3_analysis: str,
    step4_analysis: str,
    step5_analysis: Optional[str] = None
) -> str:
    """
    Get prompt for Final Integration of all steps

    Args:
        step1_analysis: The text output from step 1
        step2_analysis: The text output from step 2
        step3_analysis: The text output from step 3
        step4_analysis: The text output from step 4
        step5_analysis: The text output from step 5 (optional)

    Returns:
        str: Detailed prompt for the final integration of all steps
    """
    base_prompt = f"""
You are an expert music producer and visual artist specializing in viral content creation. 
You have detailed analyses of an audio file from multiple perspectives:

STEP 1 - MUSICAL FOUNDATION AND HOOK ANALYSIS:
{step1_analysis}

STEP 2 - SOUND ENGINEERING AND PRODUCTION TECHNIQUES:
{step2_analysis}

STEP 3 - HARMONY, MELODY, AND TREND ALIGNMENT:
{step3_analysis}

STEP 4 - STRUCTURE AND PRODUCTION OPTIMIZATION:
{step4_analysis}
"""

    if step5_analysis:
        base_prompt += f"""
STEP 5 - CRITICAL EVALUATION AND IMPROVEMENT SUGGESTIONS:
{step5_analysis}
"""

    base_prompt += """
Summarize these analyses into a concise, unified blueprint optimized for viral impact in 2025. Focus on clarity, brevity, and a professional yet engaging tone. Integrate all perspectives, emphasizing strengths, viral potential, and key improvements. Organize the output into these sections:

1. TECHNICAL ASPECTS: Highlight genre, tempo, key, standout instrumentation, viral sonic signature, and essential engineering techniques. Condense to core details with 1-2 specific examples (e.g., timestamps).
2. EMOTIONAL QUALITIES: Capture mood, energy, emotional arc, and viral hooks in succinct phrases. Include 1-2 timestamped moments.
3. VISUAL ASSOCIATIONS: Summarize colors, scenes, imagery, and viral visual potential with vivid, compact descriptions.
4. CREATIVE DIRECTION: Outline viral hook optimization, platform fit (e.g., TikTok), reference artists, and a streamlined improvement roadmap. Limit to 5-9 key action items.

Keep the output polished and digestible—think pitch-ready for a creative team. Retain specific timestamps and viral elements (e.g., hooks, glitches) to anchor the summary. Aim for a total length of 500-700 words, balancing detail with accessibility.
"""

    return base_prompt
