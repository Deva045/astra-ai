"""
Custom exceptions for the Nexus AI voice subsystem.
"""


class VoiceError(Exception):
    """Base exception for all voice-related errors."""


class AudioError(VoiceError):
    """Raised when an audio operation fails."""


class SpeechToTextError(VoiceError):
    """Raised when speech recognition fails."""


class TextToSpeechError(VoiceError):
    """Raised when speech synthesis fails."""


class WakeWordError(VoiceError):
    """Raised when wake-word detection fails."""
