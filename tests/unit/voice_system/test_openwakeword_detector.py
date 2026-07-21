"""
Unit tests for the OpenWakeWordDetector backend.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from voice.backends.openwakeword_detector import (
    OpenWakeWordDetector,
)
from voice.exceptions import WakeWordError


@patch(
    "voice.backends.openwakeword_detector.Path.exists",
    return_value=True,
)
def test_backend_initializes(mock_exists) -> None:
    """Backend should initialize correctly."""

    backend = OpenWakeWordDetector("model.tflite")

    assert backend.threshold == 0.5
    assert backend.is_running is False


@patch(
    "voice.backends.openwakeword_detector.Path.exists",
    return_value=False,
)
def test_missing_model(mock_exists) -> None:
    """Missing wake-word model should raise."""

    with pytest.raises(WakeWordError):
        OpenWakeWordDetector("missing.tflite")


@patch(
    "voice.backends.openwakeword_detector.Path.exists",
    return_value=True,
)
@patch("openwakeword.model.Model")
def test_start(
    mock_model,
    mock_exists,
) -> None:
    """Detector should start successfully."""

    backend = OpenWakeWordDetector("model.tflite")

    backend.start()

    assert backend.is_running is True
    mock_model.assert_called_once()


@patch(
    "voice.backends.openwakeword_detector.Path.exists",
    return_value=True,
)
@patch("openwakeword.model.Model")
def test_stop(
    mock_model,
    mock_exists,
) -> None:
    """Detector should stop successfully."""

    backend = OpenWakeWordDetector("model.tflite")

    backend.start()
    backend.stop()

    assert backend.is_running is False


@patch(
    "voice.backends.openwakeword_detector.Path.exists",
    return_value=True,
)
@patch("openwakeword.model.Model")
def test_detected_true(
    mock_model,
    mock_exists,
) -> None:
    """Prediction above threshold should detect wake word."""

    model = MagicMock()
    model.predict.return_value = {
        "nexus": 0.91,
    }

    mock_model.return_value = model

    backend = OpenWakeWordDetector("model.tflite")

    backend.start()

    detected = backend.process([0] * 1600)

    assert detected is True
    assert backend.detected() is True


@patch(
    "voice.backends.openwakeword_detector.Path.exists",
    return_value=True,
)
@patch("openwakeword.model.Model")
def test_detected_false(
    mock_model,
    mock_exists,
) -> None:
    """Prediction below threshold should not detect."""

    model = MagicMock()
    model.predict.return_value = {
        "nexus": 0.12,
    }

    mock_model.return_value = model

    backend = OpenWakeWordDetector("model.tflite")

    backend.start()

    detected = backend.process([0] * 1600)

    assert detected is False
    assert backend.detected() is False


@patch(
    "voice.backends.openwakeword_detector.Path.exists",
    return_value=True,
)
def test_process_without_start(
    mock_exists,
) -> None:
    """Calling process before start should raise."""

    backend = OpenWakeWordDetector("model.tflite")

    with pytest.raises(WakeWordError):
        backend.process([0] * 1600)


@patch(
    "voice.backends.openwakeword_detector.Path.exists",
    return_value=True,
)
@patch("openwakeword.model.Model")
def test_reset(
    mock_model,
    mock_exists,
) -> None:
    """Reset should clear detection state."""

    model = MagicMock()
    model.predict.return_value = {
        "nexus": 0.95,
    }

    mock_model.return_value = model

    backend = OpenWakeWordDetector("model.tflite")

    backend.start()

    backend.process([0] * 1600)

    assert backend.detected() is True

    backend.reset()

    assert backend.detected() is False
