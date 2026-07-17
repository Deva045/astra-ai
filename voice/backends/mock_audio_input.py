"""
Mock microphone backend.

This backend is intended for unit testing and development.
It provides deterministic audio data without requiring
actual microphone hardware.
"""

from __future__ import annotations

from voice.interfaces import AudioInput
from voice.models import AudioChunk


class MockAudioInput(AudioInput):
    """
    Mock implementation of the AudioInput interface.

    This backend simulates microphone input and is used
    exclusively for testing and development.
    """

    DEFAULT_SAMPLE_RATE = 16000
    DEFAULT_CHANNELS = 1
    DEFAULT_SAMPLE_WIDTH = 2

    def __init__(self) -> None:
        self._running = False
        self._chunks_read = 0

    @property
    def is_running(self) -> bool:
        """
        Return whether the mock microphone is active.
        """
        return self._running

    @property
    def chunks_read(self) -> int:
        """
        Return the number of audio chunks produced.
        """
        return self._chunks_read

    def start(self) -> None:
        """
        Start the mock microphone.
        """
        self._running = True

    def stop(self) -> None:
        """
        Stop the mock microphone.
        """
        self._running = False

    def read(self) -> AudioChunk:
        """
        Return a deterministic audio chunk.

        Returns
        -------
        AudioChunk
            Simulated microphone data.
        """
        if not self._running:
            raise RuntimeError(
                "MockAudioInput is not running."
            )

        self._chunks_read += 1

        return AudioChunk(
            data=b"\x00" * 1024,
            sample_rate=self.DEFAULT_SAMPLE_RATE,
            channels=self.DEFAULT_CHANNELS,
            sample_width=self.DEFAULT_SAMPLE_WIDTH,
        )

    def reset(self) -> None:
        """
        Reset the backend.
        """
        self._running = False
        self._chunks_read = 0
