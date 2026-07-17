"""
Microphone manager for the Nexus AI voice subsystem.

This module provides a backend-independent microphone manager.
Concrete audio backends will be integrated in later steps while
keeping this API stable.
"""

from __future__ import annotations

from typing import Optional

from .audio_manager import AudioManager
from .exceptions import AudioError
from .interfaces import AudioInput
from .models import AudioChunk


class MicrophoneManager:
    """
    Manages microphone lifecycle.

    The manager delegates actual microphone operations to an
    AudioInput implementation, allowing different audio
    backends to be plugged in without changing higher-level code.
    """

    def __init__(
        self,
        audio_manager: AudioManager,
        audio_input: Optional[AudioInput] = None,
    ) -> None:
        self._audio_manager = audio_manager
        self._audio_input = audio_input
        self._is_recording = False

    @property
    def is_recording(self) -> bool:
        """Return whether recording is currently active."""
        return self._is_recording

    @property
    def audio_input(self) -> Optional[AudioInput]:
        """Return the configured audio input backend."""
        return self._audio_input

    def set_audio_input(self, audio_input: AudioInput) -> None:
        """
        Register the microphone backend.

        Args:
            audio_input:
                Concrete implementation of AudioInput.
        """
        self._audio_input = audio_input

    def start(self) -> None:
        """
        Start microphone recording.

        Raises:
            AudioError:
                If no backend has been configured.
        """
        if self._audio_input is None:
            raise AudioError(
                "No audio input backend has been configured."
            )

        if self._is_recording:
            return

        self._audio_input.start()
        self._is_recording = True

    def stop(self) -> None:
        """
        Stop microphone recording.

        Safe to call multiple times.
        """
        if self._audio_input is None:
            return

        if not self._is_recording:
            return

        self._audio_input.stop()
        self._is_recording = False

    def read_chunk(self) -> AudioChunk:
        """
        Read a single chunk of microphone audio.

        Returns:
            AudioChunk

        Raises:
            AudioError:
                If recording has not started.
        """
        if self._audio_input is None:
            raise AudioError(
                "No audio input backend has been configured."
            )

        if not self._is_recording:
            raise AudioError(
                "Microphone is not currently recording."
            )

        return self._audio_input.read()

    def reset(self) -> None:
        """
        Reset the microphone manager.

        Stops recording if necessary and removes
        the configured backend.
        """
        self.stop()
        self._audio_input = None
