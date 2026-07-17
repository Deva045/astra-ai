"""
SoundDevice speaker backend.

This module provides audio playback using the `sounddevice`
library while implementing the AudioOutput interface.
"""

from __future__ import annotations

import threading

import numpy as np
import sounddevice as sd

from voice.exceptions import AudioError
from voice.interfaces import AudioOutput
from voice.models import AudioChunk


class SoundDeviceOutput(AudioOutput):
    """
    Audio output backend using sounddevice.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()

    def play(self, audio: AudioChunk) -> None:
        """
        Play one AudioChunk.
        """
        if not audio.data:
            raise AudioError("Audio chunk is empty.")

        samples = np.frombuffer(
            audio.data,
            dtype=np.int16,
        )

        if audio.channels > 1:
            samples = samples.reshape(
                -1,
                audio.channels,
            )

        with self._lock:
            try:
                sd.play(
                    samples,
                    samplerate=audio.sample_rate,
                )
                sd.wait()
            except Exception as exc:
                raise AudioError(
                    f"Audio playback failed: {exc}"
                ) from exc

    @staticmethod
    def available_devices() -> list[dict]:
        """
        Return all available audio devices.
        """
        try:
            return list(sd.query_devices())
        except Exception as exc:
            raise AudioError(
                f"Unable to query audio devices: {exc}"
            ) from exc

    @staticmethod
    def default_output_device() -> int | None:
        """
        Return the default output device index.
        """
        try:
            default = sd.default.device

            if default is None:
                return None

            return default[1]
        except Exception:
            return None
