"""
Unit tests for MockAudioInput.
"""

from __future__ import annotations

import pytest

from voice.backends.mock_audio_input import MockAudioInput
from voice.models import AudioChunk


def test_initial_state() -> None:
    """MockAudioInput should initialize correctly."""
    backend = MockAudioInput()

    assert backend.is_running is False
    assert backend.chunks_read == 0


def test_start() -> None:
    """Backend should start successfully."""
    backend = MockAudioInput()

    backend.start()

    assert backend.is_running is True


def test_stop() -> None:
    """Backend should stop successfully."""
    backend = MockAudioInput()

    backend.start()
    backend.stop()

    assert backend.is_running is False


def test_read_chunk() -> None:
    """Reading should return a valid AudioChunk."""
    backend = MockAudioInput()

    backend.start()

    chunk = backend.read()

    assert isinstance(chunk, AudioChunk)
    assert chunk.sample_rate == 16000
    assert chunk.channels == 1
    assert chunk.sample_width == 2
    assert len(chunk.data) == 1024


def test_chunks_read_counter() -> None:
    """Chunk counter should increase after every read."""
    backend = MockAudioInput()

    backend.start()

    backend.read()
    backend.read()
    backend.read()

    assert backend.chunks_read == 3


def test_read_without_start() -> None:
    """Reading before start should fail."""
    backend = MockAudioInput()

    with pytest.raises(RuntimeError):
        backend.read()


def test_double_start() -> None:
    """Calling start twice should be safe."""
    backend = MockAudioInput()

    backend.start()
    backend.start()

    assert backend.is_running is True


def test_double_stop() -> None:
    """Calling stop twice should be safe."""
    backend = MockAudioInput()

    backend.start()

    backend.stop()
    backend.stop()

    assert backend.is_running is False


def test_reset() -> None:
    """Reset should restore the initial state."""
    backend = MockAudioInput()

    backend.start()

    backend.read()
    backend.read()

    backend.reset()

    assert backend.is_running is False
    assert backend.chunks_read == 0


def test_multiple_cycles() -> None:
    """Multiple start/stop cycles should work."""
    backend = MockAudioInput()

    for _ in range(5):
        backend.start()

        chunk = backend.read()

        assert isinstance(chunk, AudioChunk)

        backend.stop()

    assert backend.chunks_read == 5
