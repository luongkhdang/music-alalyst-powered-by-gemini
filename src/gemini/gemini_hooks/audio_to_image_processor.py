"""
gemini_hooks/audio_to_image_processor.py - Audio to Image Processing Orchestrator

This module provides a comprehensive processor that manages the entire audio-to-image workflow.
It connects the audio analysis and image generation components into one seamless pipeline.

Related files:
- src/gemini/gemini_hooks/audio_processor.py: For audio analysis
- src/gemini/gemini_hooks/image_processor.py: For image generation
- src/gemini/gemini_client.py: Main client
"""

import os
import json
import time
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

# Import from our prompt module
from src.gemini.gemini_prompts import (
    get_audio_analysis_prompt,
    get_step1_prompt,
    get_step2_prompt,
    get_step3_prompt,
    get_step4_prompt,
    get_step5_prompt,
    get_final_integration_prompt
)

from src.gemini.gemini_prompts.generation_prompts import (
    get_image_prompt_from_audio,
    get_image_generation_prompt
)

# Import processor classes
from src.gemini.gemini_hooks.audio_processor import AudioProcessor
from src.gemini.gemini_hooks.image_processor import ImageProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
RATE_LIMIT_PAUSE = 5  # seconds to pause between API calls


class AudioToImageProcessor:
    """Processor for converting audio files into images"""

    def __init__(self, client=None):
        """
        Initialize the processor with a Gemini client

        Args:
            client: GeminiClient instance
        """
        self.client = client

        # Initialize sub-processors
        self.audio_processor = AudioProcessor(client=client)
        self.image_processor = ImageProcessor(client=client)

        # Output directories (created when needed)
        self.output_dir = Path("output")
        self.analysis_dir = self.output_dir / "analysis"
        self.image_dir = self.output_dir / "images"
        self.prompt_dir = self.image_dir / "prompts"

        # Create output directories if they don't exist
        for directory in [self.output_dir, self.analysis_dir, self.image_dir, self.prompt_dir]:
            directory.mkdir(exist_ok=True, parents=True)

        logger.info("AudioToImageProcessor initialized")

    def process_audio_file(self, audio_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Process a single audio file into an image

        Args:
            audio_path: Path to the audio file

        Returns:
            Dictionary with the analysis, prompt, and image path
        """
        if isinstance(audio_path, str):
            audio_path = Path(audio_path)

        results = {
            "audio_path": str(audio_path),
            "analysis_success": False,
            "analysis_path": None,
            "analysis_error": None,
            "prompt_success": False,
            "prompt_path": None,
            "prompt_error": None,
            "image_success": False,
            "image_path": None,
            "image_error": None
        }

        try:
            # Step 1: Perform multi-step analysis (returns path to analysis file)
            analysis_result = self.perform_multi_step_analysis(audio_path)

            # Update results with analysis outcome
            results.update(analysis_result)

            if not analysis_result.get("analysis_success", False):
                logger.error(
                    f"Analysis failed for {audio_path}, stopping processing")
                return results

            # Step 2: Generate image prompt (use the final analysis file)
            analysis_path = Path(
                analysis_result.get("final_analysis_path", ""))
            if not analysis_path.exists():
                logger.error(f"Analysis file not found: {analysis_path}")
                results["prompt_error"] = "Analysis file not found"
                return results

            # Read the analysis file
            analysis_text = analysis_path.read_text(encoding="utf-8")

            # Generate prompt
            prompt_result = self.generate_image_prompt(
                audio_path, analysis_text)
            results.update(prompt_result)

            if not prompt_result.get("prompt_success", False):
                logger.error(
                    f"Prompt generation failed for {audio_path}, stopping processing")
                return results

            # Step 3: Generate image
            prompt_path = Path(prompt_result.get("prompt_path", ""))
            if not prompt_path.exists():
                logger.error(f"Prompt file not found: {prompt_path}")
                results["image_error"] = "Prompt file not found"
                return results

            # Read the prompt file
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt_data = json.load(f)

            # Generate image
            image_result = self.generate_image(audio_path, prompt_data)
            results.update(image_result)

        except Exception as e:
            logger.exception(
                f"Error processing audio file {audio_path}: {str(e)}")
            if "analysis_error" not in results or not results["analysis_error"]:
                results["analysis_error"] = str(e)

        return results

    def process_multiple_files(self, audio_paths: List[Union[str, Path]]) -> List[Dict[str, Any]]:
        """
        Process multiple audio files into images

        Args:
            audio_paths: List of paths to audio files

        Returns:
            List of dictionaries with the analysis, prompt, and image path for each file
        """
        results = []

        for audio_path in audio_paths:
            logger.info(f"Processing audio file: {audio_path}")
            result = self.process_audio_file(audio_path)
            results.append(result)

            # Add a small pause between processing to avoid rate limits
            time.sleep(RATE_LIMIT_PAUSE)

        # Create a summary
        success_count = sum(
            1 for r in results if r.get("image_success", False))
        logger.info(
            f"Processed {len(results)} files, {success_count} successful")

        return results

    def clean_output_directories(self):
        """Clean output directories used for analysis and images"""
        # Clean analysis directory
        if self.analysis_dir.exists():
            for file_path in self.analysis_dir.glob("*.*"):
                if file_path.is_file():
                    file_path.unlink()

        # Clean image directory (keep the prompts subfolder)
        if self.image_dir.exists():
            for file_path in self.image_dir.glob("*.*"):
                if file_path.is_file():
                    file_path.unlink()

        # Clean prompts directory
        if self.prompt_dir.exists():
            for file_path in self.prompt_dir.glob("*.*"):
                if file_path.is_file():
                    file_path.unlink()

        logger.info("Output directories cleaned")

    def perform_multi_step_analysis(self, audio_path: Path) -> Dict[str, Any]:
        """
        Perform a comprehensive five-step analysis of the audio file.

        Steps:
        1. Step 1: Musical Foundation and Hook Analysis
        2. Step 2: Sound Engineering and Production Techniques (builds on Step 1)
        3. Step 3: Harmony, Melody, and Trend Alignment (builds on Steps 1 & 2)
        4. Step 4: Structure and Production Optimization (builds on Steps 1, 2 & 3)
        5. Step 5: Critical Evaluation and Improvement Suggestions (builds on Steps 1-4)
        6. Final Analysis: Comprehensive merge of all five analyses

        Args:
            audio_path: Path to the audio file

        Returns:
            Dictionary with paths to all analysis files
        """
        # Initialize results dictionary
        results = {
            "analysis_success": False,
            "analysis_error": None,
            "step1_analysis_path": None,
            "step2_analysis_path": None,
            "step3_analysis_path": None,
            "step4_analysis_path": None,
            "step5_analysis_path": None,
            "final_analysis_path": None
        }

        try:
            # Ensure output directories exist
            self.analysis_dir.mkdir(exist_ok=True, parents=True)

            # Check if the audio file exists
            if not audio_path.exists():
                logger.error(f"Audio file not found: {audio_path}")
                results["analysis_error"] = "Audio file not found"
                return results

            # Define the path for the analysis files
            step1_analysis_path = self.analysis_dir / \
                f"{audio_path.stem}_step1_analysis.txt"
            step2_analysis_path = self.analysis_dir / \
                f"{audio_path.stem}_step2_analysis.txt"
            step3_analysis_path = self.analysis_dir / \
                f"{audio_path.stem}_step3_analysis.txt"
            step4_analysis_path = self.analysis_dir / \
                f"{audio_path.stem}_step4_analysis.txt"
            step5_analysis_path = self.analysis_dir / \
                f"{audio_path.stem}_step5_analysis.txt"
            final_analysis_path = self.analysis_dir / \
                f"{audio_path.stem}_analysis.txt"

            # Check if we already have all the analyses
            if (step1_analysis_path.exists() and
                step2_analysis_path.exists() and
                step3_analysis_path.exists() and
                step4_analysis_path.exists() and
                step5_analysis_path.exists() and
                    final_analysis_path.exists()):

                logger.info(f"Using existing analysis files for {audio_path}")
                results.update({
                    "analysis_success": True,
                    "step1_analysis_path": str(step1_analysis_path),
                    "step2_analysis_path": str(step2_analysis_path),
                    "step3_analysis_path": str(step3_analysis_path),
                    "step4_analysis_path": str(step4_analysis_path),
                    "step5_analysis_path": str(step5_analysis_path),
                    "final_analysis_path": str(final_analysis_path)
                })
                return results

            # STEP 1: Musical Foundation and Hook Analysis
            logger.info(f"Performing Step 1 analysis for {audio_path}")
            step1_prompt = get_step1_prompt()

            # Custom analyze_audio that includes the MP3 title in the Discord message
            step1_analysis = self._analyze_audio_with_title(
                audio_path=audio_path,
                prompt=step1_prompt,
                temperature=0.4,
                step_name="Step 1: Musical Foundation and Hook Analysis"
            )

            # Save the analysis to file
            step1_analysis_path.write_text(step1_analysis, encoding="utf-8")
            logger.info(f"Step 1 analysis saved to {step1_analysis_path}")
            results["step1_analysis_path"] = str(step1_analysis_path)

            # Pause to respect API rate limits
            time.sleep(RATE_LIMIT_PAUSE)

            # STEP 2: Sound Engineering and Production Techniques
            logger.info(f"Performing Step 2 analysis for {audio_path}")
            step2_prompt = get_step2_prompt(step1_analysis)

            # Generate content with MP3 title included
            step2_analysis = self._generate_content_with_title(
                prompt=step2_prompt,
                temperature=0.4,
                audio_path=audio_path,
                step_name="Step 2: Sound Engineering and Production Techniques"
            )

            # Save the analysis to file
            step2_analysis_path.write_text(step2_analysis, encoding="utf-8")
            logger.info(f"Step 2 analysis saved to {step2_analysis_path}")
            results["step2_analysis_path"] = str(step2_analysis_path)

            # Pause to respect API rate limits
            time.sleep(RATE_LIMIT_PAUSE)

            # STEP 3: Harmony, Melody, and Trend Alignment
            logger.info(f"Performing Step 3 analysis for {audio_path}")
            step3_prompt = get_step3_prompt(step1_analysis, step2_analysis)

            # Generate content with MP3 title included
            step3_analysis = self._generate_content_with_title(
                prompt=step3_prompt,
                temperature=0.4,
                audio_path=audio_path,
                step_name="Step 3: Harmony, Melody, and Trend Alignment"
            )

            # Save the analysis to file
            step3_analysis_path.write_text(step3_analysis, encoding="utf-8")
            logger.info(f"Step 3 analysis saved to {step3_analysis_path}")
            results["step3_analysis_path"] = str(step3_analysis_path)

            # Pause to respect API rate limits
            time.sleep(RATE_LIMIT_PAUSE)

            # STEP 4: Structure and Production Optimization
            logger.info(f"Performing Step 4 analysis for {audio_path}")
            step4_prompt = get_step4_prompt(
                step1_analysis, step2_analysis, step3_analysis)

            # Generate content with MP3 title included
            step4_analysis = self._generate_content_with_title(
                prompt=step4_prompt,
                temperature=0.4,
                audio_path=audio_path,
                step_name="Step 4: Structure and Production Optimization"
            )

            # Save the analysis to file
            step4_analysis_path.write_text(step4_analysis, encoding="utf-8")
            logger.info(f"Step 4 analysis saved to {step4_analysis_path}")
            results["step4_analysis_path"] = str(step4_analysis_path)

            # Pause to respect API rate limits
            time.sleep(RATE_LIMIT_PAUSE)

            # STEP 5: Critical Evaluation and Improvement Suggestions
            logger.info(f"Performing Step 5 analysis for {audio_path}")
            step5_prompt = get_step5_prompt(
                step1_analysis, step2_analysis, step3_analysis, step4_analysis)

            # Generate content with MP3 title included
            step5_analysis = self._generate_content_with_title(
                prompt=step5_prompt,
                temperature=0.4,
                audio_path=audio_path,
                step_name="Step 5: Critical Evaluation and Improvement Suggestions"
            )

            # Save the analysis to file
            step5_analysis_path.write_text(step5_analysis, encoding="utf-8")
            logger.info(f"Step 5 analysis saved to {step5_analysis_path}")
            results["step5_analysis_path"] = str(step5_analysis_path)

            # Pause to respect API rate limits
            time.sleep(RATE_LIMIT_PAUSE)

            # FINAL ANALYSIS: Integrate all analyses into a comprehensive analysis
            logger.info(
                f"Performing final integration analysis for {audio_path}")
            final_prompt = get_final_integration_prompt(
                step1_analysis, step2_analysis, step3_analysis, step4_analysis, step5_analysis
            )

            # Generate content with MP3 title included
            final_analysis = self._generate_content_with_title(
                prompt=final_prompt,
                temperature=0.4,
                audio_path=audio_path,
                step_name="Final Integrated Analysis"
            )

            # Save the analysis to file
            final_analysis_path.write_text(final_analysis, encoding="utf-8")
            logger.info(f"Final analysis saved to {final_analysis_path}")
            results["final_analysis_path"] = str(final_analysis_path)

            # Mark analysis as successful
            results["analysis_success"] = True

        except Exception as e:
            logger.exception(
                f"Error performing multi-step analysis for {audio_path}: {str(e)}")
            results["analysis_error"] = str(e)

        return results

    def _analyze_audio_with_title(self, audio_path: Path, prompt: str, temperature: float = 0.4,
                                  step_name: str = "Audio Analysis") -> str:
        """
        Analyze audio content with a text prompt and include the MP3 title in the Discord message.

        Args:
            audio_path: Path to the audio file
            prompt: Text prompt to guide the analysis
            temperature: Controls randomness (0.0-2.0)
            step_name: Name of the analysis step for Discord message

        Returns:
            Analysis text
        """
        # Use analyze_audio from the client, but customize the source parameter
        response_text = self.client.analyze_audio(
            audio_path_or_file=audio_path,
            prompt=prompt,
            temperature=temperature
        )

        # Send to Discord with a custom source that includes the MP3 title
        source_with_title = f"{step_name} | {audio_path.name}"

        # Use the client's _send_to_discord method to send the result to Discord
        self.client._send_to_discord(
            response=response_text,
            prompt=prompt,
            is_final=True,
            source=source_with_title,
            content_type="audio analysis"
        )

        return response_text

    def _generate_content_with_title(self, prompt: str, temperature: float = 0.4,
                                     audio_path: Path = None, step_name: str = "Content Generation") -> str:
        """
        Generate content with a text prompt and include the MP3 title in the Discord message.

        Args:
            prompt: Text prompt to generate content from
            temperature: Controls randomness (0.0-2.0)
            audio_path: Path to the audio file for inclusion in Discord message
            step_name: Name of the generation step for Discord message

        Returns:
            Generated text
        """
        # Use generate_content from Gemini client
        response_text = self.client.generate_content(
            prompt=prompt,
            temperature=temperature
        )

        # Send to Discord with a custom source that includes the MP3 title
        if audio_path:
            source_with_title = f"{step_name} | {audio_path.name}"
        else:
            source_with_title = step_name

        # Use the client's _send_to_discord method to send the result to Discord
        self.client._send_to_discord(
            response=response_text,
            prompt=prompt,
            is_final=True,
            source=source_with_title,
            content_type="text"
        )

        return response_text

    def generate_image_prompt(self, audio_path: Path, analysis_text: str) -> Dict[str, Any]:
        """
        Generate an image prompt based on the audio analysis

        Args:
            audio_path: Path to the audio file
            analysis_text: The text analysis of the audio

        Returns:
            Dictionary with the prompt path
        """
        results = {
            "prompt_success": False,
            "prompt_path": None,
            "prompt_error": None
        }

        try:
            # Ensure output directories exist
            self.prompt_dir.mkdir(exist_ok=True, parents=True)

            # Get the prompt template
            prompt_template = get_image_generation_prompt(analysis_text)

            # Generate the prompt content with title in Discord message
            prompt_content = self._generate_content_with_title(
                prompt=prompt_template,
                temperature=0.7,
                audio_path=audio_path,
                step_name="Image Prompt Generation"
            )

            # Clean the prompt content - check for markdown code blocks and extract just the JSON
            cleaned_content = prompt_content
            # Check for markdown JSON code block
            if "```json" in prompt_content:
                # Extract content between ```json and ```
                import re
                json_match = re.search(
                    r'```json\s*(.*?)\s*```', prompt_content, re.DOTALL)
                if json_match:
                    cleaned_content = json_match.group(1).strip()
            # Or just a regular code block
            elif "```" in prompt_content:
                # Extract content between ``` and ```
                import re
                json_match = re.search(
                    r'```\s*(.*?)\s*```', prompt_content, re.DOTALL)
                if json_match:
                    cleaned_content = json_match.group(1).strip()

            try:
                # Try to parse as JSON
                prompt_data = json.loads(cleaned_content)

                # Add timestamp and audio filename
                import datetime
                prompt_data["timestamp"] = datetime.datetime.now().isoformat()
                prompt_data["audio_file"] = audio_path.name

                # Write the prompt to file
                prompt_path = self.prompt_dir / \
                    f"{audio_path.stem}_prompt.json"
                with open(prompt_path, "w", encoding="utf-8") as f:
                    json.dump(prompt_data, f, indent=2)

                logger.info(f"Image prompt saved to {prompt_path}")
                results["prompt_success"] = True
                results["prompt_path"] = str(prompt_path)

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse prompt as JSON: {str(e)}")
                logger.error(f"Raw content: {prompt_content}")
                logger.error(f"Cleaned content: {cleaned_content}")

                # Save the raw content for debugging
                raw_path = self.prompt_dir / \
                    f"{audio_path.stem}_raw_prompt.txt"
                with open(raw_path, "w", encoding="utf-8") as f:
                    f.write(prompt_content)

                results["prompt_error"] = f"JSON parse error: {str(e)}"

        except Exception as e:
            logger.exception(
                f"Error generating image prompt for {audio_path}: {str(e)}")
            results["prompt_error"] = str(e)

        return results

    def generate_image(self, audio_path: Path, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an image based on the prompt

        Args:
            audio_path: Path to the audio file
            prompt_data: Dictionary with prompt data

        Returns:
            Dictionary with the image path
        """
        results = {
            "image_success": False,
            "image_path": None,
            "image_error": None
        }

        try:
            # Ensure output directories exist
            self.image_dir.mkdir(exist_ok=True, parents=True)

            # Get the main prompt from the data
            main_prompt = prompt_data.get("prompt", "")
            if not main_prompt:
                raise ValueError("Prompt does not contain a 'prompt' field")

            # Generate the image
            description_text, image = self.client.generate_image(
                main_prompt, temperature=0.9)

            # Send the description to Discord with MP3 title included
            source_with_title = f"Image Generation | {audio_path.name}"
            self.client._send_to_discord(
                response=description_text if description_text else "Image generated successfully",
                prompt=main_prompt,
                is_final=True,
                source=source_with_title,
                content_type="image generation"
            )

            # Save the image
            image_path = self.image_dir / f"{audio_path.stem}_image.png"
            image.save(image_path)

            logger.info(f"Image saved to {image_path}")
            results["image_success"] = True
            results["image_path"] = str(image_path)

        except Exception as e:
            logger.exception(
                f"Error generating image for {audio_path}: {str(e)}")
            results["image_error"] = str(e)

        return results
