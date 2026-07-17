"""
SoundDevice microphone backend.

Provides microphone capture using the sounddevice library while
implementing the AudioInput interface.
"""

from __future__ import annotations

import threading

import numpy as np
import sounddevice as sd

from voice.exceptions import AudioError
from voice.interfaces import AudioInput
from voice.models import AudioChunk


class SoundDeviceInput(AudioInput):
    """
    Real microphone backend using sounddevice.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_size: int = 1024,
        device: int | None = None,
    ) -> None:
        self._sample_rate = sample_rate
        self._channels = channels
        self._chunk_size = chunk_size
        self._device = device

        self._stream: sd.InputStream | None = None
        self._running = False
        self._lock = threading.Lock()

    @property
    def is_running(self) -> bool:
        """
        Return whether the microphone is active.
        """
        return self._running

    def start(self) -> None:
        """
        Start capturing microphone audio.
        """
        if self._running:
            return

        try:
            self._stream = sd.InputStream(
                samplerate=self._sample_rate,
                channels=self._channels,
                dtype="int16",
                blocksize=self._chunk_size,
                device=self._device,
            )

            self._stream.start()
            self._running = True

        except Exception as exc:
            raise AudioError(
                f"Unable to start microphone: {exc}"
            ) from exc

    def stop(self) -> None:
        """
        Stop microphone capture.
        """
        if not self._running:
            return

        with self._lock:
            if self._stream is not None:
                self._stream.stop()
                self._stream.close()
                self._stream = None

            self._running = False

    def read(self) -> AudioChunk:
        """
        Read one chunk of microphone audio.
        """
        if not self._running:
            raise AudioError(
                "Microphone has not been started."
            )

        if self._stream is None:
            raise AudioError(
                "Input stream is unavailable."
            )

        try:
            samples, overflowed = self._stream.read(
                self._chunk_size
            )

            if overflowed:
                raise AudioError(
                    "Audio input overflow."
                )

            audio_bytes = (
                np.asarray(
                    samples,
                    dtype=np.int16,
                ).tobytes()
            )

            return AudioChunk(
                data=audio_bytes,
                sample_rate=self._sample_rate,
                channels=self._channels,
                sample_width=2,
            )

        except Exception as exc:
            raise AudioError(
                f"Unable to read microphone: {exc}"
            ) from exc

    def reset(self) -> None:
        """
        Reset the backend.
        """
        self.stop()

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
    def default_input_device() -> int | None:
        """
        Return the default input device index.
        """
        try:
            default = sd.default.device

            if default is None:
                return None

            return default[0]
        except Exception:
            return None
