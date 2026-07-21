"""
Speech-to-Text manager for the Nexus AI voice subsystem.

This module provides a backend-independent Speech-to-Text (STT)
manager. Concrete implementations (e.g. Vosk, Faster-Whisper,
Whisper.cpp) will be added later without changing this interface.
"""

from __future__ import annotations

from typing import Optional

from .exceptions import SpeechToTextError
from .interfaces import SpeechToText
from .models import AudioChunk


class SpeechToTextManager:
    """
    Coordinates speech recognition using a pluggable backend.

    The manager delegates transcription to a concrete
    SpeechToText implementation.
    """

    def __init__(
        self,
        backend: Optional[SpeechToText] = None,
    ) -> None:
        self._backend = backend

    @property
    def backend(self) -> Optional[SpeechToText]:
        """Return the configured STT backend."""
        return self._backend

    def set_backend(self, backend: SpeechToText) -> None:
        """
        Configure the STT backend.

        Args:
            backend:
                Concrete implementation of the SpeechToText interface.
        """
        self._backend = backend

    def has_backend(self) -> bool:
        """Return True if an STT backend has been configured."""
        return self._backend is not None

    def transcribe(self, audio: AudioChunk) -> str:
        """
        Convert an audio chunk into text.

        Args:
            audio:
                Audio to transcribe.

        Returns:
            Recognized text.

        Raises:
            SpeechToTextError:
                If no backend is configured or the backend
                returns invalid output.
        """
        if self._backend is None:
            raise SpeechToTextError(
                "No Speech-to-Text backend has been configured."
            )

        text = self._backend.transcribe(audio)

        if not isinstance(text, str):
            raise SpeechToTextError(
                "Speech-to-Text backend returned an invalid result."
            )

        return text.strip()

    def reset(self) -> None:
        """Remove the configured backend."""
        self._backend = None
