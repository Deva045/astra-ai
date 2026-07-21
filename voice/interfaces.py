"""
Abstract interfaces for the Nexus AI voice subsystem.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .models import AudioChunk


class SpeechToText(ABC):
    """Speech-to-text provider interface."""

    @abstractmethod
    def transcribe(self, audio: AudioChunk) -> str:
        """Convert audio into text."""


class TextToSpeech(ABC):
    """Text-to-speech provider interface."""

    @abstractmethod
    def speak(self, text: str) -> None:
        """Speak the supplied text."""


class WakeWordDetector(ABC):
    """Wake-word detection interface."""

    @abstractmethod
    def start(self) -> None:
        """Start wake-word detection."""

    @abstractmethod
    def stop(self) -> None:
        """Stop wake-word detection."""

    @abstractmethod
    def detected(self) -> bool:
        """Return True when the wake word has been detected."""


class AudioInput(ABC):
    """Microphone interface."""

    @abstractmethod
    def start(self) -> None:
        """Start capturing audio."""

    @abstractmethod
    def stop(self) -> None:
        """Stop capturing audio."""

    @abstractmethod
    def read(self) -> AudioChunk:
        """Read a single chunk of audio."""


class AudioOutput(ABC):
    """Speaker interface."""

    @abstractmethod
    def play(self, audio: AudioChunk) -> None:
        """Play an audio chunk."""
