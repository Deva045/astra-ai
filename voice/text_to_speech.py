"""
Text-to-Speech manager for the Nexus AI voice subsystem.

This module provides a backend-independent Text-to-Speech (TTS)
manager. Concrete implementations (e.g. Piper, pyttsx3, Coqui TTS)
will be added later without changing this interface.
"""

from __future__ import annotations

from typing import Optional

from .exceptions import TextToSpeechError
from .interfaces import TextToSpeech


class TextToSpeechManager:
    """
    Coordinates speech synthesis using a pluggable backend.

    The manager delegates speech synthesis to a concrete
    TextToSpeech implementation.
    """

    def __init__(
        self,
        backend: Optional[TextToSpeech] = None,
    ) -> None:
        self._backend = backend

    @property
    def backend(self) -> Optional[TextToSpeech]:
        """Return the configured TTS backend."""
        return self._backend

    def set_backend(self, backend: TextToSpeech) -> None:
        """
        Configure the Text-to-Speech backend.

        Args:
            backend:
                Concrete implementation of the TextToSpeech interface.
        """
        self._backend = backend

    def has_backend(self) -> bool:
        """Return True if a backend has been configured."""
        return self._backend is not None

    def speak(self, text: str) -> None:
        """
        Convert text into spoken audio.

        Args:
            text:
                Text to speak.

        Raises:
            TextToSpeechError:
                If no backend is configured or the input is invalid.
        """
        if self._backend is None:
            raise TextToSpeechError(
                "No Text-to-Speech backend has been configured."
            )

        if not isinstance(text, str):
            raise TextToSpeechError(
                "Text must be a string."
            )

        text = text.strip()

        if not text:
            raise TextToSpeechError(
                "Cannot speak empty text."
            )

        self._backend.speak(text)

    def stop(self) -> None:
        """
        Stop speech output.

        This method is reserved for future backends that
        support interrupting speech playback.
        """
        # Reserved for future implementation.
        return

    def reset(self) -> None:
        """Remove the configured backend."""
        self._backend = None
