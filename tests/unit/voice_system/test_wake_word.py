"""
Unit tests for the WakeWordManager.
"""

from __future__ import annotations

import pytest

from voice.exceptions import WakeWordError
from voice.interfaces import WakeWordDetector
from voice.wake_word import WakeWordManager


class DummyWakeWordDetector(WakeWordDetector):
    """Simple WakeWord detector used for testing."""

    def __init__(self) -> None:
        self.started = False
        self.stopped = False
        self.detected_value = False

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True

    def detected(self) -> bool:
        return self.detected_value


def test_initial_state() -> None:
    """Manager should initialize correctly."""
    manager = WakeWordManager()

    assert manager.backend is None
    assert manager.is_running is False
    assert manager.has_backend() is False


def test_set_backend() -> None:
    """Backend should be registered."""
    backend = DummyWakeWordDetector()

    manager = WakeWordManager()

    manager.set_backend(backend)

    assert manager.backend is backend
    assert manager.has_backend() is True


def test_start() -> None:
    """Wake-word detection should start."""
    backend = DummyWakeWordDetector()

    manager = WakeWordManager(backend)

    manager.start()

    assert manager.is_running is True
    assert backend.started is True


def test_stop() -> None:
    """Wake-word detection should stop."""
    backend = DummyWakeWordDetector()

    manager = WakeWordManager(backend)

    manager.start()
    manager.stop()

    assert manager.is_running is False
    assert backend.stopped is True


def test_detect_true() -> None:
    """Detection should return True."""
    backend = DummyWakeWordDetector()
    backend.detected_value = True

    manager = WakeWordManager(backend)

    manager.start()

    assert manager.detect() is True


def test_detect_false() -> None:
    """Detection should return False."""
    backend = DummyWakeWordDetector()

    manager = WakeWordManager(backend)

    manager.start()

    assert manager.detect() is False


def test_start_without_backend() -> None:
    """Starting without backend should fail."""
    manager = WakeWordManager()

    with pytest.raises(WakeWordError):
        manager.start()


def test_detect_without_backend() -> None:
    """Detection without backend should fail."""
    manager = WakeWordManager()

    with pytest.raises(WakeWordError):
        manager.detect()


def test_detect_when_not_running() -> None:
    """Detection before start should fail."""
    backend = DummyWakeWordDetector()

    manager = WakeWordManager(backend)

    with pytest.raises(WakeWordError):
        manager.detect()


def test_double_start() -> None:
    """Calling start twice should be safe."""
    backend = DummyWakeWordDetector()

    manager = WakeWordManager(backend)

    manager.start()
    manager.start()

    assert manager.is_running is True


def test_double_stop() -> None:
    """Calling stop twice should be safe."""
    backend = DummyWakeWordDetector()

    manager = WakeWordManager(backend)

    manager.start()

    manager.stop()
    manager.stop()

    assert manager.is_running is False


def test_reset() -> None:
    """Reset should stop detection and remove backend."""
    backend = DummyWakeWordDetector()

    manager = WakeWordManager(backend)

    manager.start()

    manager.reset()

    assert manager.backend is None
    assert manager.is_running is False
    assert manager.has_backend() is False
