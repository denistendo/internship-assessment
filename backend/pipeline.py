"""
Pipeline orchestrator that handles the complete workflow:
Input -> STT (if audio) -> Summarize -> Translate -> TTS -> Output
"""

import os
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
from backend.sunbird_client import SunbirdClient, SunbirdAPIError


class ProcessingPipeline:
    """Orchestrates the text processing pipeline with Sunbird AI."""
    
    SUPPORTED_LANGUAGES = {
        "Luganda": "lg",
        "Runyankole": "ny",
        "Ateso": "teo",
        "Lugbara": "lgg",
        "Acholi": "ach"
    }
    
    MAX_AUDIO_DURATION_SECONDS = 300  # 5 minutes
    
    def __init__(self):
        """Initialize the pipeline with Sunbird client."""
        self.client = SunbirdClient()
    
    def validate_audio_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Validate audio file exists and is not too large.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not os.path.exists(file_path):
            return False, "Audio file not found"
        
        file_size = os.path.getsize(file_path)
        # Rough estimate: 128 kbps audio ≈ 16 KB/sec
        # For 5 min limit: 300 sec * 16 KB ≈ 4.8 MB
        max_size_bytes = 5 * 1024 * 1024  # 5 MB
        
        if file_size > max_size_bytes:
            return False, "Audio file exceeds 5-minute limit"
        
        return True, ""
    
    def process_text_input(self, text: str) -> str:
        """
        Validate and prepare text input.
        
        Args:
            text: Input text
            
        Returns:
            Prepared text
        """
        return text.strip()
    
    def transcribe_audio(self, audio_file_path: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Transcribe audio file to text.
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Tuple of (transcript, error_message)
        """
        try:
            is_valid, error = self.validate_audio_file(audio_file_path)
            if not is_valid:
                return None, error
            
            transcript = self.client.transcribe_audio(audio_file_path)
            return transcript, None
        except SunbirdAPIError as e:
            return None, f"Transcription error: {str(e)}"
    
    def summarize_text(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Summarize text using Sunflower LLM. If text is short, bypass summarization.
        
        Args:
            text: Text to summarize
            
        Returns:
            Tuple of (summary, error_message)
        """
        # If the text is too short to be summarized, just return it as-is
        if len(text.split()) < 30:
            return text, None

        try:
            summary = self.client.summarize(text)
            return summary, None
        except SunbirdAPIError as e:
            return None, f"Summarization error: {str(e)}"
    
    def translate_text(self, text: str, target_language: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Translate text to target language.
        
        Args:
            text: Text to translate
            target_language: Target language name (e.g., "Luganda")
            
        Returns:
            Tuple of (translation, error_message)
        """
        if target_language not in self.SUPPORTED_LANGUAGES:
            return None, f"Unsupported language: {target_language}"
        
        try:
            translation = self.client.translate(text, target_language)
            return translation, None
        except SunbirdAPIError as e:
            return None, f"Translation error: {str(e)}"
    
    def synthesize_speech(self, text: str, target_language: str = "Luganda", output_path: str = "output.mp3") -> Tuple[Optional[str], Optional[str]]:
        """
        Synthesize text to speech.
        
        Args:
            text: Text to synthesize
            target_language: Target language for speech generation (e.g., "Luganda")
            output_path: Path to save audio file
            
        Returns:
            Tuple of (file_path, error_message)
        """
        try:
            file_path = self.client.synthesize_speech(text, language=target_language, output_path=output_path)
            return file_path, None
        except SunbirdAPIError as e:
            return None, f"Speech synthesis error: {str(e)}"
    
    def run_full_pipeline(
        self,
        input_type: str,
        input_data: str,
        target_language: str
    ) -> Dict[str, Any]:
        """
        Run the complete pipeline: Input -> STT (if audio) -> Summarize -> Translate -> TTS.
        
        Args:
            input_type: "text" or "audio"
            input_data: Text content or path to audio file
            target_language: Target language for translation
            
        Returns:
            Dictionary with pipeline results and any errors
        """
        results = {
            "success": False,
            "original_text": None,
            "transcript": None,
            "summary": None,
            "translation": None,
            "audio_file": None,
            "errors": []
        }
        
        try:
            # Step 1: Get input text
            if input_type == "audio":
                transcript, error = self.transcribe_audio(input_data)
                if error:
                    results["errors"].append(f"Transcription: {error}")
                    return results
                results["transcript"] = transcript
                original_text = transcript
            else:  # text
                original_text = self.process_text_input(input_data)
            
            results["original_text"] = original_text
            
            # Step 2: Summarize
            summary, error = self.summarize_text(original_text)
            if error:
                results["errors"].append(f"Summarization: {error}")
                return results
            results["summary"] = summary
            
            # Step 3: Translate
            translation, error = self.translate_text(summary, target_language)
            if error:
                results["errors"].append(f"Translation: {error}")
                return results
            results["translation"] = translation
            
            # Step 4: Synthesize speech
            audio_file, error = self.synthesize_speech(translation, target_language=target_language)
            if error:
                results["errors"].append(f"Speech synthesis: {error}")
                return results
            results["audio_file"] = audio_file
            
            results["success"] = True
            return results
        
        except Exception as e:
            results["errors"].append(f"Pipeline error: {str(e)}")
            return results
    
    @staticmethod
    def get_supported_languages() -> Dict[str, str]:
        """Get list of supported languages."""
        return ProcessingPipeline.SUPPORTED_LANGUAGES
