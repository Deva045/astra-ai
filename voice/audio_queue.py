"""
Thread-safe audio queue for the Nexus AI voice subsystem.

This module provides a producer/consumer queue for audio chunks.
It is used to decouple microphone capture, speech recognition,
wake-word detection, and audio playback.

The queue is backend-independent and can be used by any audio
implementation.
"""

from __future__ import annotations

from queue import Empty, Full, Queue

from .models import AudioChunk


class AudioQueue:
    """
    Thread-safe queue for AudioChunk objects.
    """

    DEFAULT_MAX_SIZE = 100

    def __init__(
        self,
        max_size: int = DEFAULT_MAX_SIZE,
    ) -> None:
        self._queue: Queue[AudioChunk] = Queue(
            maxsize=max_size,
        )

    @property
    def max_size(self) -> int:
        """
        Return the maximum queue size.
        """
        return self._queue.maxsize

    def put(
        self,
        chunk: AudioChunk,
        *,
        block: bool = True,
        timeout: float | None = None,
    ) -> None:
        """
        Add an audio chunk to the queue.
        """
        self._queue.put(
            chunk,
            block=block,
            timeout=timeout,
        )

    def get(
        self,
        *,
        block: bool = True,
        timeout: float | None = None,
    ) -> AudioChunk:
        """
        Remove and return an audio chunk.
        """
        return self._queue.get(
            block=block,
            timeout=timeout,
        )

    def clear(self) -> None:
        """
        Remove all queued audio.
        """
        while True:
            try:
                self._queue.get_nowait()
            except Empty:
                break

    def empty(self) -> bool:
        """
        Return True if the queue is empty.
        """
        return self._queue.empty()

    def full(self) -> bool:
        """
        Return True if the queue is full.
        """
        return self._queue.full()

    def size(self) -> int:
        """
        Return the current queue size.
        """
        return self._queue.qsize()

    def put_nowait(
        self,
        chunk: AudioChunk,
    ) -> None:
        """
        Add an audio chunk without blocking.
        """
        self._queue.put_nowait(chunk)

    def get_nowait(self) -> AudioChunk:
        """
        Remove an audio chunk without blocking.
        """
        return self._queue.get_nowait()

    def reset(self) -> None:
        """
        Reset the queue.
        """
        self.clear()


class AudioQueueFullError(Full):
    """
    Raised when the audio queue is full.
    """


class AudioQueueEmptyError(Empty):
    """
    Raised when the audio queue is empty.
    """
