"""
Unit tests for the TextToSpeechManager.
"""

from __future__ import annotations

import pytest

from voice.exceptions import TextToSpeechError
from voice.interfaces import TextToSpeech
from voice.text_to_speech import TextToSpeechManager


class DummyTextToSpeech(TextToSpeech):
    """Simple Text-to-Speech backend used for testing."""

    def __init__(self) -> None:
        self.last_text: str | None = None

    def speak(self, text: str) -> None:
        self.last_text = text


def test_initial_state() -> None:
    """Manager should initialize without a backend."""
    manager = TextToSpeechManager()

    assert manager.backend is None
    assert manager.has_backend() is False


def test_set_backend() -> None:
    """Backend should be registered correctly."""
    backend = DummyTextToSpeech()

    manager = TextToSpeechManager()

    manager.set_backend(backend)

    assert manager.backend is backend
    assert manager.has_backend() is True


def test_speak() -> None:
    """Text should be passed to the backend."""
    backend = DummyTextToSpeech()

    manager = TextToSpeechManager(backend)

    manager.speak("Hello Nexus")

    assert backend.last_text == "Hello Nexus"


def test_speak_strips_whitespace() -> None:
    """Whitespace should be removed before speaking."""
    backend = DummyTextToSpeech()

    manager = TextToSpeechManager(backend)

    manager.speak("   Hello Nexus   ")

    assert backend.last_text == "Hello Nexus"


def test_speak_without_backend() -> None:
    """Speaking without a backend should fail."""
    manager = TextToSpeechManager()

    with pytest.raises(TextToSpeechError):
        manager.speak("Hello")


def test_empty_text() -> None:
    """Empty text should not be accepted."""
    backend = DummyTextToSpeech()

    manager = TextToSpeechManager(backend)

    with pytest.raises(TextToSpeechError):
        manager.speak("")


def test_whitespace_only_text() -> None:
    """Whitespace-only text should not be accepted."""
    backend = DummyTextToSpeech()

    manager = TextToSpeechManager(backend)

    with pytest.raises(TextToSpeechError):
        manager.speak("     ")


def test_invalid_input_type() -> None:
    """Input must be a string."""
    backend = DummyTextToSpeech()

    manager = TextToSpeechManager(backend)

    with pytest.raises(TextToSpeechError):
        manager.speak(123)  # type: ignore[arg-type]


def test_stop() -> None:
    """
    stop() is currently a placeholder.

    It should execute without raising an exception.
    """
    backend = DummyTextToSpeech()

    manager = TextToSpeechManager(backend)

    manager.stop()


def test_reset() -> None:
    """Reset should remove the backend."""
    backend = DummyTextToSpeech()

    manager = TextToSpeechManager(backend)

    manager.reset()

    assert manager.backend is None
    assert manager.has_backend() is False
