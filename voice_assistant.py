"""
Voice Assistant for Krishi Sakhi
Provides voice recognition and text-to-speech functionality
"""

import streamlit as st
import time
import random
from io import BytesIO
try:
    from gtts import gTTS  # Google TTS supports 'en' and 'ml'
    GTTS_AVAILABLE = True
except Exception:
    GTTS_AVAILABLE = False

# Mock voice assistant since actual voice libraries may not be available
class VoiceAssistant:
    def __init__(self):
        self.is_listening = False
        self.is_speaking = False
        
    def listen_for_speech(self, timeout=5):
        """Mock speech recognition"""
        if not hasattr(st.session_state, 'voice_input'):
            st.session_state.voice_input = None
            
        # Simulate listening
        self.is_listening = True
        time.sleep(1)
        self.is_listening = False
        
        # Return mock recognized speech
        mock_phrases = [
            "What is the best time to plant rice?",
            "How to control pests in coconut?",
            "Show me the weather forecast",
            "What fertilizer should I use for pepper?",
            "നെല്ല് എങ്ങനെ നടാം?",
            "കാലാവസ്ഥ കാണിക്കുക"
        ]
        
        return random.choice(mock_phrases)
    
    def speak_text(self, text, language="en"):
        """Text-to-speech. Returns (success, audio_bytes or None, format)."""
        self.is_speaking = True
        try:
            if GTTS_AVAILABLE:
                lang_code = "ml" if language == "ml" else "en"
                tts = gTTS(text=text, lang=lang_code)
                buf = BytesIO()
                tts.write_to_fp(buf)
                buf.seek(0)
                self.is_speaking = False
                return True, buf.read(), "audio/mp3"
            else:
                # Fallback mock
                st.info(f"🔊 Speaking: {text}")
                time.sleep(1.5)
                self.is_speaking = False
                return True, None, None
        except Exception:
            self.is_speaking = False
            return False, None, None
    
    def is_voice_available(self):
        """Check if voice features are available"""
        return True  # Mock availability
    
    def process_voice_command(self, command):
        """Process voice command and return action"""
        command_lower = command.lower()
        
        # Navigation commands
        if any(phrase in command_lower for phrase in ['dashboard', 'home', 'ഡാഷ്ബോർഡ്']):
            return {"action": "navigate", "page": "dashboard"}
        elif any(phrase in command_lower for phrase in ['farms', 'farm', 'കൃഷിയിടം']):
            return {"action": "navigate", "page": "farms"}
        elif any(phrase in command_lower for phrase in ['weather', 'കാലാവസ്ഥ']):
            return {"action": "navigate", "page": "weather"}
        elif any(phrase in command_lower for phrase in ['disease', 'രോഗം']):
            return {"action": "navigate", "page": "disease_detection"}
        elif any(phrase in command_lower for phrase in ['chat', 'assistant', 'സഹായി']):
            return {"action": "navigate", "page": "ai_chat"}
        else:
            return {"action": "chat", "query": command}