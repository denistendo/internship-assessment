"""
Thin wrapper around Sunbird AI API endpoints.
Handles authentication, requests, and responses for:
- Speech-to-Text (STT)
- Text-to-Speech (TTS)  
- Summarization & Translation (Sunflower LLM)
"""

import os
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("SUNBIRD_API_TOKEN")
API_BASE_URL = os.getenv("SUNBIRD_API_BASE_URL", "https://api.sunbird.ai/v1")


class SunbirdAPIError(Exception):
    """Custom exception for Sunbird API errors."""
    pass


class SunbirdClient:
    """Client for interacting with Sunbird AI APIs."""
    
    def __init__(self, api_token: str = API_TOKEN, base_url: str = API_BASE_URL):
        """
        Initialize the Sunbird API client.
        
        Args:
            api_token: Sunbird API token (from .env or parameter)
            base_url: Base URL for Sunbird API
        """
        if not api_token:
            raise ValueError("SUNBIRD_API_TOKEN not found in environment variables")
        
        self.api_token = api_token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make an API request to Sunbird.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response JSON as dictionary
            
        Raises:
            SunbirdAPIError: If API request fails
        """
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("headers", self.headers)
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise SunbirdAPIError(f"API request failed: {str(e)}")
    
    def transcribe_audio(self, audio_file_path: str, language: str = "en") -> str:
        """
        Transcribe audio to text using Speech-to-Text API.
        
        Args:
            audio_file_path: Path to audio file
            language: Language code (default: "en")
            
        Returns:
            Transcribed text
            
        Raises:
            SunbirdAPIError: If transcription fails
        """
        with open(audio_file_path, "rb") as f:
            files = {"file": f}
            data = {"language": language}
            
            try:
                response = requests.post(
                    f"{self.base_url}/speech-to-text",
                    headers={"Authorization": f"Bearer {self.api_token}"},
                    files=files,
                    data=data
                )
                response.raise_for_status()
                result = response.json()
                return result.get("transcript", "")
            except requests.exceptions.RequestException as e:
                raise SunbirdAPIError(f"Transcription failed: {str(e)}")
    
    def summarize(self, text: str) -> str:
        """
        Summarize text using Sunflower LLM.
        
        Args:
            text: Text to summarize
            
        Returns:
            Summarized text
            
        Raises:
            SunbirdAPIError: If summarization fails
        """
        prompt = f"Summarize the following text concisely:\n\n{text}"
        
        payload = {
            "model": "sunflower-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            result = self._make_request("POST", "/chat", json=payload)
            # Extract summary from response
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        except SunbirdAPIError as e:
            raise SunbirdAPIError(f"Summarization failed: {str(e)}")
    
    def translate(self, text: str, target_language: str) -> str:
        """
        Translate text to target language using Sunflower LLM.
        
        Args:
            text: Text to translate
            target_language: Target language (Luganda, Runyankole, Ateso, Lugbara, Acholi)
            
        Returns:
            Translated text
            
        Raises:
            SunbirdAPIError: If translation fails
        """
        prompt = f"Translate the following text to {target_language}:\n\n{text}"
        
        payload = {
            "model": "sunflower-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            result = self._make_request("POST", "/chat", json=payload)
            # Extract translation from response
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        except SunbirdAPIError as e:
            raise SunbirdAPIError(f"Translation failed: {str(e)}")
    
    def synthesize_speech(self, text: str, language: str = "en", output_path: str = "output.mp3") -> str:
        """
        Synthesize text to speech using Text-to-Speech API.
        
        Args:
            text: Text to convert to speech
            language: Language code (default: "en")
            output_path: Path to save audio file
            
        Returns:
            Path to generated audio file
            
        Raises:
            SunbirdAPIError: If synthesis fails
        """
        data = {
            "text": text,
            "language": language
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/text-to-speech",
                headers={"Authorization": f"Bearer {self.api_token}"},
                json=data
            )
            response.raise_for_status()
            
            # Save audio file
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            return output_path
        except requests.exceptions.RequestException as e:
            raise SunbirdAPIError(f"Speech synthesis failed: {str(e)}")
