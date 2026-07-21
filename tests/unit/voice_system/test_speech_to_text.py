"""
Unit tests for the SpeechToTextManager.
"""

from __future__ import annotations

import pytest

from voice.exceptions import SpeechToTextError
from voice.interfaces import SpeechToText
from voice.models import AudioChunk
from voice.speech_to_text import SpeechToTextManager


class DummySpeechToText(SpeechToText):
    """Simple Speech-to-Text backend used for testing."""

    def transcribe(self, audio: AudioChunk) -> str:
        return "Hello Nexus"


class InvalidSpeechToText(SpeechToText):
    """Returns an invalid result."""

    def transcribe(self, audio: AudioChunk):
        return 12345


def create_audio_chunk() -> AudioChunk:
    """Create a dummy audio chunk."""
    return AudioChunk(
        data=b"audio",
        sample_rate=16000,
        channels=1,
        sample_width=2,
    )


def test_initial_state() -> None:
    """Manager should initialize without a backend."""
    manager = SpeechToTextManager()

    assert manager.backend is None
    assert manager.has_backend() is False


def test_set_backend() -> None:
    """Backend should be registered."""
    backend = DummySpeechToText()

    manager = SpeechToTextManager()

    manager.set_backend(backend)

    assert manager.backend is backend
    assert manager.has_backend() is True


def test_transcribe() -> None:
    """Audio should be transcribed."""
    backend = DummySpeechToText()

    manager = SpeechToTextManager(backend)

    text = manager.transcribe(create_audio_chunk())

    assert text == "Hello Nexus"


def test_transcribe_strips_whitespace() -> None:
    """Whitespace should be removed."""

    class Backend(SpeechToText):
        def transcribe(self, audio: AudioChunk) -> str:
            return "   Hello Nexus   "

    manager = SpeechToTextManager(Backend())

    assert manager.transcribe(create_audio_chunk()) == "Hello Nexus"


def test_transcribe_without_backend() -> None:
    """Missing backend should raise."""
    manager = SpeechToTextManager()

    with pytest.raises(SpeechToTextError):
        manager.transcribe(create_audio_chunk())


def test_invalid_backend_result() -> None:
    """Backend must return a string."""
    manager = SpeechToTextManager(
        InvalidSpeechToText()
    )

    with pytest.raises(SpeechToTextError):
        manager.transcribe(create_audio_chunk())


def test_reset() -> None:
    """Reset should remove backend."""
    backend = DummySpeechToText()

    manager = SpeechToTextManager(backend)

    manager.reset()

    assert manager.backend is None
    assert manager.has_backend() is False
