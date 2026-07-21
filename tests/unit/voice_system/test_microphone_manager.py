"""
Unit tests for the MicrophoneManager.
"""

from __future__ import annotations

import pytest

from voice.audio_manager import AudioManager
from voice.exceptions import AudioError
from voice.interfaces import AudioInput
from voice.microphone_manager import MicrophoneManager
from voice.models import AudioChunk


class DummyAudioInput(AudioInput):
    """Simple mock AudioInput implementation."""

    def __init__(self) -> None:
        self.started = False
        self.stopped = False

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True

    def read(self) -> AudioChunk:
        return AudioChunk(
            data=b"audio",
            sample_rate=16000,
            channels=1,
            sample_width=2,
        )


def test_initial_state() -> None:
    """MicrophoneManager should start idle."""
    manager = MicrophoneManager(AudioManager())

    assert manager.is_recording is False
    assert manager.audio_input is None


def test_set_audio_input() -> None:
    """Backend should be stored correctly."""
    manager = MicrophoneManager(AudioManager())

    backend = DummyAudioInput()

    manager.set_audio_input(backend)

    assert manager.audio_input is backend


def test_start_recording() -> None:
    """Recording should start successfully."""
    backend = DummyAudioInput()

    manager = MicrophoneManager(AudioManager(), backend)

    manager.start()

    assert manager.is_recording is True
    assert backend.started is True


def test_stop_recording() -> None:
    """Recording should stop successfully."""
    backend = DummyAudioInput()

    manager = MicrophoneManager(AudioManager(), backend)

    manager.start()
    manager.stop()

    assert manager.is_recording is False
    assert backend.stopped is True


def test_read_chunk() -> None:
    """Audio chunk should be returned."""
    backend = DummyAudioInput()

    manager = MicrophoneManager(AudioManager(), backend)

    manager.start()

    chunk = manager.read_chunk()

    assert isinstance(chunk, AudioChunk)
    assert chunk.data == b"audio"
    assert chunk.sample_rate == 16000


def test_start_without_backend() -> None:
    """Starting without backend should fail."""
    manager = MicrophoneManager(AudioManager())

    with pytest.raises(AudioError):
        manager.start()


def test_read_without_backend() -> None:
    """Reading without backend should fail."""
    manager = MicrophoneManager(AudioManager())

    with pytest.raises(AudioError):
        manager.read_chunk()


def test_read_without_start() -> None:
    """Reading before start should fail."""
    backend = DummyAudioInput()

    manager = MicrophoneManager(AudioManager(), backend)

    with pytest.raises(AudioError):
        manager.read_chunk()


def test_double_start() -> None:
    """Calling start twice should be safe."""
    backend = DummyAudioInput()

    manager = MicrophoneManager(AudioManager(), backend)

    manager.start()
    manager.start()

    assert manager.is_recording is True


def test_double_stop() -> None:
    """Calling stop twice should be safe."""
    backend = DummyAudioInput()

    manager = MicrophoneManager(AudioManager(), backend)

    manager.start()

    manager.stop()
    manager.stop()

    assert manager.is_recording is False


def test_reset() -> None:
    """Reset should stop recording and clear backend."""
    backend = DummyAudioInput()

    manager = MicrophoneManager(AudioManager(), backend)

    manager.start()

    manager.reset()

    assert manager.is_recording is False
    assert manager.audio_input is None
