"""
Audio manager for the Nexus AI voice subsystem.

This module is responsible for managing audio configuration and
validating audio settings. It intentionally contains no platform-
specific or third-party audio implementation. Concrete backends
(e.g. sounddevice, PyAudio, etc.) will be added later while keeping
this interface unchanged.
"""

from __future__ import annotations

from dataclasses import replace

from .exceptions import AudioError
from .models import VoiceSettings


class AudioManager:
    """
    Manages audio configuration for the voice subsystem.

    This class is backend-independent. It stores and validates
    audio settings but does not access microphones or speakers.
    """

    MIN_SAMPLE_RATE = 8_000
    MAX_SAMPLE_RATE = 48_000

    MIN_CHANNELS = 1
    MAX_CHANNELS = 2

    MIN_CHUNK_SIZE = 256
    MAX_CHUNK_SIZE = 8_192

    def __init__(self, settings: VoiceSettings | None = None) -> None:
        """
        Initialize the audio manager.

        Args:
            settings:
                Optional voice settings. If omitted, default
                VoiceSettings are used.
        """
        self._settings = settings or VoiceSettings()
        self._validate(self._settings)

    @property
    def settings(self) -> VoiceSettings:
        """
        Return a copy of the current settings.

        Returning a copy prevents accidental external mutation.
        """
        return replace(self._settings)

    def update_settings(self, settings: VoiceSettings) -> None:
        """
        Replace the current audio configuration.

        Args:
            settings:
                New validated settings.

        Raises:
            AudioError:
                If the supplied settings are invalid.
        """
        self._validate(settings)
        self._settings = settings

    def set_input_device(self, device: str | None) -> None:
        """Set the preferred microphone device."""
        self._settings.input_device = device

    def set_output_device(self, device: str | None) -> None:
        """Set the preferred speaker device."""
        self._settings.output_device = device

    def get_input_device(self) -> str | None:
        """Return the configured microphone device."""
        return self._settings.input_device

    def get_output_device(self) -> str | None:
        """Return the configured speaker device."""
        return self._settings.output_device

    def supports_streaming(self) -> bool:
        """
        Indicates whether streaming is supported.

        Streaming will be implemented in a later sprint.
        """
        return False

    def reset(self) -> None:
        """Restore default voice settings."""
        self._settings = VoiceSettings()

    def _validate(self, settings: VoiceSettings) -> None:
        """Validate voice configuration."""

        if not (
            self.MIN_SAMPLE_RATE
            <= settings.sample_rate
            <= self.MAX_SAMPLE_RATE
        ):
            raise AudioError(
                f"Sample rate must be between "
                f"{self.MIN_SAMPLE_RATE} and "
                f"{self.MAX_SAMPLE_RATE} Hz."
            )

        if not (
            self.MIN_CHANNELS
            <= settings.channels
            <= self.MAX_CHANNELS
        ):
            raise AudioError(
                f"Channels must be between "
                f"{self.MIN_CHANNELS} and "
                f"{self.MAX_CHANNELS}."
            )

        if not (
            self.MIN_CHUNK_SIZE
            <= settings.chunk_size
            <= self.MAX_CHUNK_SIZE
        ):
            raise AudioError(
                f"Chunk size must be between "
                f"{self.MIN_CHUNK_SIZE} and "
                f"{self.MAX_CHUNK_SIZE}."
            )

        if settings.speech_timeout <= 0:
            raise AudioError(
                "Speech timeout must be greater than zero."
            )

        if settings.silence_timeout <= 0:
            raise AudioError(
                "Silence timeout must be greater than zero."
            )
