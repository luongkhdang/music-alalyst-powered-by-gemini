"""
gemini_prompts/refinement_prompt.py - Critical Musical Foundation Specialist refinement prompts

Provides prompts for the 5-step refinery process in the audio analysis pipeline:
- get_refinery_analyst1_prompt(final_analysis): Musical Foundation Specialist verification
- get_refinery_analyst2_prompt(final_analysis): Engineering Specialist verification
- get_refinery_analyst3_prompt(final_analysis): Harmony and Melody Specialist verification
- get_refinery_analyst4_prompt(final_analysis): Structure Specialist verification
- get_refinery_analyst5_prompt(final_analysis): Critical Evaluator verification
- get_refinement_prompt(final_analysis): Comprehensive refinement (backward compatibility)
- get_final_refinery_prompt(analyst1_output, analyst2_output, analyst3_output, analyst4_output, analyst5_output):
  Final validation and cross-checking by Summary and Validation Expert

This refinement step has Gemini act as multiple specialized musical experts
to verify the accuracy of the final analysis before proceeding to image generation.

Related files:
- src/gemini/gemini_hooks/audio_to_image_processor.py: Uses these prompts for refinement
- src/gemini/gemini_prompts/multi_step_analysis_prompts.py: For the earlier analysis steps
- src/gemini/gemini_client.py: Main client that orchestrates the analysis
"""
from typing import Optional


def get_refinery_analyst1_prompt(final_analysis: str) -> str:
    """
    Get prompt for Refinery Analyst 1: Musical Foundation Specialist

    Focuses on verifying genre, tempo, key, mood, instrumentation, hooks.

    Args:
        final_analysis: The text output from the final integration analysis

    Returns:
        str: Detailed prompt for the Musical Foundation Specialist verification
    """
    return f"""
You are Refinery Analyst 1: an extremely critical Musical Foundation Specialist with decades of experience in music theory, production, and analysis. You specialize in genre identification, tempo analysis, key detection, mood assessment, instrumentation identification, and hook analysis.
!IMPORTANT: Listen to the provided audio file at least 6 times to ensure a thorough understanding.
!IMPORTANT: Listen to the provided audio file at least 6 times to verify and critique the analysis.
Your task is to critically evaluate the accuracy of the following music analysis, focusing exclusively on the core musical foundation elements:

FINAL ANALYSIS:
{final_analysis}

Now, listen to the audio track again with fresh ears and a highly critical mindset. Focus exclusively on:

1. GENRE VERIFICATION:
   - Cross-check genre and sub-genre classifications against established definitions
   - Verify if the genre fusion claims (if any) are accurate
   - Test if platform categorizations (e.g., "TikTok-ready trap") are musically justifiable

2. TEMPO & RHYTHM PRECISION:
   - Verify exact tempo (BPM) measurements to within 0.1 BPM precision
   - Confirm time signature identifications
   - Validate rhythm pattern identifications and groove classifications
   - Test for tempo variations or changes that might have been missed

3. KEY & TONALITY SCRUTINY:
   - Confirm key signature claims (e.g., is it truly in F# Minor or actually A Major?)
   - Verify modal claims (e.g., Dorian, Mixolydian)
   - Test for key changes or modulations that may have been overlooked
   - Assess if tonal characteristics are accurately described

4. MOOD ASSESSMENT VERIFICATION:
   - Question whether the emotional qualities described actually align with the sonic reality
   - Test claims about intended mood against actual listener impact
   - Verify if mood progression and emotional arcs are accurately mapped

5. INSTRUMENTATION ANALYSIS:
   - Verify instrument identifications with certainty
   - Test frequency ranges attributed to instruments (e.g., "sub-bass at 40 Hz")
   - Confirm if layering and instrument combinations are accurately identified

6. HOOK EVALUATION:
   - Verify the identified hooks are truly the most impactful elements
   - Test hook placement timestamps for accuracy
   - Assess if hook descriptions match their actual sonic characteristics

Use the following methodology:
- Audio signal analysis: Listen critically multiple times, focusing on individual elements
- Trend database cross-referencing: Compare to established genre conventions and current trends

For each element analyzed, provide:
- Confirmation of accurate claims with precise supporting evidence
- Correction of any inaccuracies with technically sound explanations
- Additional nuance that may have been overlooked
- Specific timestamps and measurements to support your analysis

Your output should be approximately 6,000 tokens of raw analysis, presenting the gold standard of musical foundation analysis with absolute technical precision.
"""


def get_refinery_analyst2_prompt(final_analysis: str) -> str:
    """
    Get prompt for Refinery Analyst 2: Engineering Specialist

    Focuses on verifying frequency balance, stereo imaging, transients, production techniques.

    Args:
        final_analysis: The text output from the final integration analysis

    Returns:
        str: Detailed prompt for the Engineering Specialist verification
    """
    return f"""
You are Refinery Analyst 2: an extremely critical Engineering Specialist with decades of experience in sound engineering, mixing, mastering, and audio production. You specialize in frequency analysis, stereo imaging, transient shaping, and production technique identification.
!IMPORTANT: Listen to the provided audio file at least 6 times to ensure a thorough understanding.
!IMPORTANT: Listen to the provided audio file at least 6 times to verify and critique the analysis.
Your task is to critically evaluate the accuracy of the following music analysis, focusing exclusively on the engineering and production elements:

FINAL ANALYSIS:
{final_analysis}

Now, listen to the audio track again with fresh ears and a highly critical mindset. Focus exclusively on:

1. FREQUENCY BALANCE VERIFICATION:
   - Verify frequency distribution claims across sub-bass, bass, low-mids, mids, high-mids, and highs
   - Test EQ claims and frequency carving assertions
   - Confirm resonances, notches, or frequency buildups that are mentioned or overlooked
   - Assess if spectral balance descriptions match actual sonic reality

2. STEREO IMAGING SCRUTINY:
   - Verify stereo width claims for specific elements and frequency bands
   - Test spatial positioning statements for accuracy
   - Confirm panning automation and movement descriptions
   - Assess if immersive audio characteristics are accurately described

3. TRANSIENT ANALYSIS:
   - Verify attack and decay characteristics of percussive elements
   - Test claims about transient shaping techniques
   - Confirm if punch, snap, and impact assessments are accurate
   - Assess if dynamic processing on transients is correctly identified

4. PRODUCTION TECHNIQUES VERIFICATION:
   - Test all claims about production techniques (e.g., sidechain compression, parallel processing)
   - Verify signal chain descriptions and effect ordering
   - Confirm automation claims (filters, volume, modulation)
   - Scrutinize engineering claims (e.g., compression ratios, EQ decisions, reverb settings)

5. SOUND DESIGN ASSESSMENT:
   - Verify synthesis technique identifications
   - Test claims about sound manipulation and processing
   - Confirm described textures and timbres against actual sonic characteristics
   - Assess if unique sound design elements are accurately documented

Use the following methodology:
- Spectral analysis: Critically assess frequency content, stereo information, and transient behavior
- Engineering benchmarks: Compare against established production standards and techniques

For each element analyzed, provide:
- Confirmation of accurate engineering claims with precise supporting evidence
- Correction of any technical inaccuracies with detailed explanations
- Additional production insights that may have been overlooked
- Specific measurements (e.g., dB levels, frequency points, ratio settings) to support your analysis

Your output should be approximately 6,000 tokens of raw analysis, presenting the gold standard of audio engineering analysis with absolute technical precision.
"""


def get_refinery_analyst3_prompt(final_analysis: str) -> str:
    """
    Get prompt for Refinery Analyst 3: Harmony and Melody Specialist

    Focuses on verifying chord progressions, melodic lines, trend alignment.

    Args:
        final_analysis: The text output from the final integration analysis

    Returns:
        str: Detailed prompt for the Harmony and Melody Specialist verification
    """
    return f"""
You are Refinery Analyst 3: an extremely critical Harmony and Melody Specialist with decades of experience in music theory, composition, and trend analysis. You specialize in harmonic analysis, melodic evaluation, and alignment with current and emerging music trends.
!IMPORTANT: Listen to the provided audio file at least 6 times to ensure a thorough understanding.
!IMPORTANT: Listen to the provided audio file at least 6 times to verify and critique the analysis.
Your task is to critically evaluate the accuracy of the following music analysis, focusing exclusively on the harmonic, melodic, and trend elements:

FINAL ANALYSIS:
{final_analysis}

Now, listen to the audio track again with fresh ears and a highly critical mindset. Focus exclusively on:

1. CHORD PROGRESSION VERIFICATION:
   - Verify chord identification accuracy (e.g., Cm7, F#maj9, G7sus4)
   - Test progression analyses and functional harmony claims
   - Confirm voicing descriptions (open, closed, inversions)
   - Assess if harmonic rhythm is accurately described
   - Verify any claims about borrowed chords, secondary dominants, or modal interchange

2. MELODIC STRUCTURE SCRUTINY:
   - Verify melodic contour descriptions and shape analyses
   - Test interval relationships and scale usage claims
   - Confirm if repetition patterns and thematic development are accurately identified
   - Assess if melodic hooks are properly highlighted
   - Verify note choice and phrasing characterizations

3. HARMONIC-MELODIC RELATIONSHIP ANALYSIS:
   - Verify how melodies interact with underlying chord progressions
   - Test tension and release claims in the harmonic-melodic relationship
   - Confirm counterpoint and voice leading observations
   - Assess if melodic dissonance and consonance are properly documented

4. TREND ALIGNMENT VERIFICATION:
   - Test claims about current (2025) musical trends
   - Verify if genre-specific harmonic and melodic conventions are accurately identified
   - Confirm if platform-specific musical characteristics are correctly assessed
   - Assess accuracy of comparisons to contemporary artists or songs
   - Verify predictions about trend longevity or trajectory

5. CREATIVE INNOVATION ASSESSMENT:
   - Verify claims about musical innovation or uniqueness
   - Test if harmonic or melodic elements described as "standout" truly are distinctive
   - Confirm if fusion elements are accurately characterized
   - Assess if experimental aspects are properly contextualized

Use the following methodology:
- Music theory parsing: Analyze the harmonic and melodic content through formal music theory
- 2025 trend forecasting: Compare to current trends and anticipate near-future developments

For each element analyzed, provide:
- Confirmation of accurate harmonic and melodic claims with precise supporting evidence
- Correction of any music theory inaccuracies with detailed explanations
- Additional harmonic and melodic insights that may have been overlooked
- Specific musical notations, timestamps, and trend references to support your analysis

Your output should be approximately 6,000 tokens of raw analysis, presenting the gold standard of harmony, melody, and trend analysis with absolute music theory precision.
"""


def get_refinery_analyst4_prompt(final_analysis: str) -> str:
    """
    Get prompt for Refinery Analyst 4: Structure Specialist

    Focuses on verifying arrangement, texture, production polish.

    Args:
        final_analysis: The text output from the final integration analysis

    Returns:
        str: Detailed prompt for the Structure Specialist verification
    """
    return f"""
You are Refinery Analyst 4: an extremely critical Structure Specialist with decades of experience in music arrangement, production, and platform optimization. You specialize in structural analysis, textural evaluation, and production polish assessment.
!IMPORTANT: Listen to the provided audio file at least 6 times to ensure a thorough understanding.
!IMPORTANT: Listen to the provided audio file at least 6 times to verify and critique the analysis.
Your task is to critically evaluate the accuracy of the following music analysis, focusing exclusively on the structural, textural, and polish elements:

FINAL ANALYSIS:
{final_analysis}

Now, listen to the audio track again with fresh ears and a highly critical mindset. Focus exclusively on:

1. ARRANGEMENT STRUCTURE VERIFICATION:
   - Verify section identification accuracy (e.g., intro, verse, chorus, bridge)
   - Test section length measurements and transition points
   - Confirm structural patterns and form analysis
   - Assess if narrative structure and energy flow are accurately mapped
   - Verify claims about traditional or experimental arrangement choices

2. TEXTURE DENSITY SCRUTINY:
   - Verify texture density descriptions throughout various sections
   - Test layering analysis and arrangement complexity claims
   - Confirm if textural contrasts and variations are accurately documented
   - Assess if the relationship between density and energy is properly characterized
   - Verify claims about textural uniqueness or conventionality

3. DYNAMIC STRUCTURE ANALYSIS:
   - Verify loudness mapping and dynamic range assessments
   - Test claims about dynamic contrasts between sections
   - Confirm if micro-dynamics within sections are accurately described
   - Assess if build-ups, drops, and releases are properly documented
   - Verify RMS levels, peak measurements, and dynamic processing observations

4. PRODUCTION POLISH VERIFICATION:
   - Test claims about final mix clarity and cohesion
   - Verify mastering assessments and loudness normalization observations
   - Confirm if transition smoothness evaluations are accurate
   - Assess if overall sonic consistency claims match reality
   - Verify observations about professional finish quality

5. PLATFORM OPTIMIZATION ASSESSMENT:
   - Verify claims about loopability for short-form content
   - Test hook placement optimization for streaming platforms
   - Confirm if attention-grabbing elements are accurately identified
   - Assess if claims about platform-specific structure optimization are valid
   - Verify statements about section adaptability for edits and remixes

Use the following methodology:
- Timeline mapping: Analyze the structural organization and flow of the track
- Platform optimization algorithms: Evaluate against best practices for various platforms

For each element analyzed, provide:
- Confirmation of accurate structural and textural claims with precise supporting evidence
- Correction of any arrangement or polish inaccuracies with detailed explanations
- Additional structural and textural insights that may have been overlooked
- Specific timestamps, section measurements, and platform-specific references to support your analysis

Your output should be approximately 6,000 tokens of raw analysis, presenting the gold standard of structure, texture, and polish analysis with absolute production precision.
"""


def get_refinery_analyst5_prompt(final_analysis: str) -> str:
    """
    Get prompt for Refinery Analyst 5: Critical Evaluator

    Focuses on verifying critiques and improvement suggestions.

    Args:
        final_analysis: The text output from the final integration analysis

    Returns:
        str: Detailed prompt for the Critical Evaluator verification
    """
    return f"""
You are Refinery Analyst 5: an extremely critical Evaluator with decades of experience in music production, A&R, and market analysis. You specialize in identifying strengths and weaknesses, suggesting strategic improvements, and assessing commercial and artistic potential.
!IMPORTANT: Listen to the provided audio file at least 6 times to ensure a thorough understanding.
!IMPORTANT: Listen to the provided audio file at least 6 times to verify and critique the analysis.     
Your task is to critically evaluate the accuracy and effectiveness of the critique and suggestions in the following music analysis:

FINAL ANALYSIS:
{final_analysis}

Now, listen to the audio track again with fresh ears and a highly critical mindset. Focus exclusively on:

1. CRITIQUE ACCURACY VERIFICATION:
   - Verify if identified weaknesses are genuine limitations of the track
   - Test if the severity of issues is accurately represented
   - Confirm if the described strengths are truly standout qualities
   - Assess if the balance between positives and negatives is justified
   - Verify if technical critiques are factually accurate and relevant

2. IMPROVEMENT SUGGESTIONS SCRUTINY:
   - Test if proposed improvements would actually enhance the track
   - Verify if suggested techniques are appropriate for the style and goals
   - Confirm if the technical advice is sound and implementable
   - Assess if alternative approaches might yield better results
   - Verify if the suggested prioritization of improvements is strategic

3. COMMERCIAL POTENTIAL ANALYSIS:
   - Verify assessments of market fit and audience appeal
   - Test claims about viral potential and platform suitability
   - Confirm if comparisons to successful tracks are apt and insightful
   - Assess if commercial weaknesses and opportunities are accurately identified
   - Verify statements about trend alignment and market timing

4. ARTISTIC INTEGRITY EVALUATION:
   - Verify if critique preserves or enhances the artistic vision
   - Test if suggested changes respect the core identity of the track
   - Confirm if the balance between commercial and artistic considerations is appropriate
   - Assess if unique creative elements are properly valued
   - Verify if the artistic trajectory suggested aligns with current creative directions

5. TECHNICAL FEASIBILITY ASSESSMENT:
   - Verify if the suggested improvements are technically achievable
   - Test if the production advice requires unreasonable resources
   - Confirm if the technical critiques account for practical limitations
   - Assess if implementation complexity is accurately represented
   - Verify if alternative technical approaches could be more efficient

Use the following methodology:
- Comparative analysis: Evaluate against 2025's top tracks and production benchmarks
- Technical synthesis: Integrate perspectives across foundational, engineering, harmonic/melodic, and structural dimensions

For each element analyzed, provide:
- Confirmation of valid critiques and suggestions with precise supporting evidence
- Correction of any misguided or impractical feedback with detailed explanations
- Additional critical insights and improvement strategies that may have been overlooked
- Specific examples, references, and techniques to support your evaluation

Your output should be approximately 6,000 tokens of raw analysis, presenting the gold standard of critical evaluation with absolute professional precision.
"""


def get_final_refinery_prompt(
    analyst1_output: str,
    analyst2_output: str,
    analyst3_output: str,
    analyst4_output: str,
    analyst5_output: str,
    final_analysis: Optional[str] = None
) -> str:
    """
    Get prompt for Final Refinery: Summary and Validation Expert

    Cross-checks facts, resolves discrepancies, and distills into a final polished summary.

    Args:
        analyst1_output: Output from the Musical Foundation Specialist
        analyst2_output: Output from the Engineering Specialist
        analyst3_output: Output from the Harmony and Melody Specialist
        analyst4_output: Output from the Structure Specialist
        analyst5_output: Output from the Critical Evaluator
        final_analysis: The original final analysis (optional)

    Returns:
        str: Detailed prompt for the final refinery process
    """
    base_prompt = f"""
You are the Refinery AI: a Summary and Validation Expert with exceptional skills in cross-referencing, fact-checking, and synthesizing complex musical analyses. You excel at resolving contradictions, identifying consensus, and distilling extensive technical information into clear, actionable insights.
!IMPORTANT: Listen to the provided audio file at least 6 times to ensure a thorough understanding.
!IMPORTANT: Listen to the provided audio file at least 6 times to verify and critique the analysis.
Your task is to cross-check facts, resolve discrepancies, and distill the following specialist analyses into a final polished summary:

ANALYST 1 - MUSICAL FOUNDATION SPECIALIST:
{analyst1_output}

ANALYST 2 - ENGINEERING SPECIALIST:
{analyst2_output}

ANALYST 3 - HARMONY AND MELODY SPECIALIST:
{analyst3_output}

ANALYST 4 - STRUCTURE SPECIALIST:
{analyst4_output}

ANALYST 5 - CRITICAL EVALUATOR:
{analyst5_output}
"""

    if final_analysis:
        base_prompt += f"""
ORIGINAL FINAL ANALYSIS:
{final_analysis}
"""

    base_prompt += """
Conduct a comprehensive cross-check and validation, focusing on:

1. FACT CONSISTENCY:
   - Verify if Analyst 1's tempo matches Analyst 2's transient patterns
   - Check if Analyst 1's key assessment aligns with Analyst 3's harmonic analysis
   - Confirm if Analyst 1's mood characterization is supported by Analyst 3's melodic findings
   - Validate if Analyst 1's hook identification matches Analyst 4's structural highlights
   - Ensure Analyst 2's frequency balance assessment aligns with Analyst 3's harmonic texture analysis

2. DISCREPANCY RESOLUTION:
   - Identify any contradictions between analyst findings
   - Weigh competing analyses based on supporting evidence and specificity
   - Resolve conflicts through majority consensus or strength of evidence
   - When necessary, suggest a qualified resolution that acknowledges uncertainty
   - Prioritize precision over generalization when addressing discrepancies

3. SUMMARY SYNTHESIS:
   - Distill approximately 30,000 tokens of specialist analysis into a 500-700 word blueprint
   - Balance technical precision with accessible language
   - Ensure all key insights are represented proportionally to their importance
   - Maintain the critical perspective while presenting a unified assessment
   - Create a document that's immediately useful for creative decision-making

Organize your final output into these sections:

1. TECHNICAL ASPECTS: Highlight the most accurately verified information about genre, tempo, key, standout instrumentation, viral sonic signature, and essential engineering techniques. Condense to core details with 1-2 specific examples (e.g., timestamps).

2. EMOTIONAL QUALITIES: Capture the most definitively verified mood, energy, emotional arc, and viral hooks in succinct phrases. Include 1-2 timestamped moments that all analysts agree upon.

3. VISUAL ASSOCIATIONS: Summarize the most compellingly justified colors, scenes, imagery, and viral visual potential with vivid, compact descriptions that align with the verified sonic characteristics.

4. CREATIVE DIRECTION: Outline viral hook optimization, platform fit (e.g., TikTok), reference artists, and a streamlined improvement roadmap based on the most convincingly validated suggestions. Limit to 5-9 key action items with clear consensus.

Keep the output polished and digestible—think pitch-ready for a creative team. Retain specific timestamps and viral elements (e.g., hooks, glitches) to anchor the summary. Aim for a total length of 500-700 words, balancing detail with accessibility.

This final refinement represents the absolute verified truth about the track, with all claims thoroughly cross-checked and validated across multiple specialist perspectives.
"""
    return base_prompt


def get_refinement_prompt(final_analysis: str) -> str:
    """
    Get prompt for Refinement Step: Critical Musical Foundation Specialist Review
    (Maintained for backward compatibility)

    Args:
        final_analysis: The text output from the final integration analysis

    Returns:
        str: Detailed prompt for the refinement step that critically evaluates the accuracy of the final analysis
    """
    return f"""
You are an extremely critical Musical Foundation Specialist with decades of experience in music theory, production, and analysis. You are renowned for your exacting standards and your ability to spot even the slightest inaccuracies in musical analysis.

Your task is to critically evaluate the accuracy of the following comprehensive music analysis, challenging assumptions, verifying technical claims, and assessing whether the analysis truly captures the essence of the track.

FINAL ANALYSIS:
{final_analysis}

Now, listen to the audio track again with fresh ears and a highly critical mindset. Focus on:

1. TECHNICAL ACCURACY:
   - Verify exact tempo (BPM) measurements to within 0.1 BPM precision
   - Confirm key signature and tonality claims (e.g., is it truly in F# Minor or actually A Major?)
   - Validate time signature and rhythm pattern identifications
   - Cross-check genre and sub-genre classifications against established definitions
   - Verify frequency specifications (e.g., "sub-bass at 40 Hz") with spectral analysis precision

2. PRODUCTION FACT-CHECKING:
   - Test all claims about production techniques (e.g., sidechain compression, stereo imaging)
   - Verify instrument identifications and sound design descriptions
   - Challenge assumptions about software, plugins, or hardware used in production
   - Scrutinize engineering claims (e.g., compression ratios, EQ decisions)

3. EMOTIONAL ASSESSMENT VERIFICATION:
   - Question whether the emotional qualities described actually align with the sonic reality
   - Verify that timestamp references to emotional shifts are accurate
   - Test claims about intended mood against actual listener impact

4. CREATIVE POTENTIAL REALITY CHECK:
   - Challenge assumptions about viral potential and platform suitability
   - Verify that suggested improvements are actually technically sound
   - Assess whether the track truly has the qualities claimed in the analysis

For each section of the analysis, provide:
- Confirmation of accurate elements
- Correction of any inaccuracies with precise, technically sound explanations
- Nuance or complexity that may have been overlooked
- Alternative interpretations where the original analysis might be subjective

Be ruthlessly accurate but fair. Your goal is not to dismiss the original analysis, but to refine it to a level of absolute technical precision and musical truth. Include specific timestamps, frequency measurements, and musical notation examples where relevant to support your critique.

Your refined analysis should represent the gold standard of musical analysis, leaving no room for technical inaccuracies or unfounded claims.
"""
