"""
Nexus AI Voice System.

Provides the public API for the voice subsystem.
"""

from .assistant import AIEngineVoiceAssistant, VoiceAssistant
from .exceptions import (
    AudioError,
    SpeechToTextError,
    TextToSpeechError,
    VoiceError,
    WakeWordError,
)
from .models import (
    AudioChunk,
    VoiceSettings,
    VoiceState,
)

__all__ = [
    "AIEngineVoiceAssistant",
    "VoiceAssistant",
    "VoiceError",
    "AudioError",
    "SpeechToTextError",
    "TextToSpeechError",
    "WakeWordError",
    "AudioChunk",
    "VoiceSettings",
    "VoiceState",
]
