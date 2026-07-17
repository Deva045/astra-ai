"""
Unit tests for the PiperTextToSpeech backend.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import subprocess
import pytest

from voice.backends.piper_tts import PiperTextToSpeech
from voice.exceptions import TextToSpeechError


@patch("voice.backends.piper_tts.Path.exists", return_value=True)
def test_backend_initializes(mock_exists) -> None:
    """Backend should initialize correctly."""

    backend = PiperTextToSpeech(
        executable="piper",
        model_path="voice.onnx",
    )

    assert backend.executable == Path("piper")
    assert backend.model_path == Path("voice.onnx")
    assert backend.output_file == Path("piper_output.wav")


@patch("voice.backends.piper_tts.Path.exists", return_value=False)
def test_missing_executable(mock_exists) -> None:
    """Missing executable should raise."""

    with pytest.raises(TextToSpeechError):
        PiperTextToSpeech(
            executable="missing",
            model_path="voice.onnx",
        )


@patch("voice.backends.piper_tts.Path.exists")
def test_missing_model(mock_exists) -> None:
    """Missing model should raise."""

    mock_exists.side_effect = [True, False]

    with pytest.raises(TextToSpeechError):
        PiperTextToSpeech(
            executable="piper",
            model_path="missing.onnx",
        )


@patch("voice.backends.piper_tts.subprocess.run")
@patch("voice.backends.piper_tts.Path.exists", return_value=True)
def test_speak_success(
    mock_exists,
    mock_run,
) -> None:
    """Speech synthesis should invoke Piper."""

    backend = PiperTextToSpeech(
        executable="piper",
        model_path="voice.onnx",
    )

    backend.speak("Hello Nexus")

    mock_run.assert_called_once()


@patch("voice.backends.piper_tts.Path.exists", return_value=True)
def test_empty_text(mock_exists) -> None:
    """Empty text should raise."""

    backend = PiperTextToSpeech(
        executable="piper",
        model_path="voice.onnx",
    )

    with pytest.raises(TextToSpeechError):
        backend.speak("")


@patch("voice.backends.piper_tts.Path.exists", return_value=True)
def test_invalid_text(mock_exists) -> None:
    """Non-string input should raise."""

    backend = PiperTextToSpeech(
        executable="piper",
        model_path="voice.onnx",
    )

    with pytest.raises(TextToSpeechError):
        backend.speak(None)  # type: ignore[arg-type]


@patch("voice.backends.piper_tts.subprocess.run")
@patch("voice.backends.piper_tts.Path.exists", return_value=True)
def test_piper_failure(
    mock_exists,
    mock_run,
) -> None:
    """Piper errors should be wrapped."""

    mock_run.side_effect = subprocess.CalledProcessError(
        returncode=1,
        cmd="piper",
        stderr=b"failure",
    )

    backend = PiperTextToSpeech(
        executable="piper",
        model_path="voice.onnx",
    )

    with pytest.raises(TextToSpeechError):
        backend.speak("Hello")


@patch("voice.backends.piper_tts.subprocess.run")
@patch("voice.backends.piper_tts.Path.exists", return_value=True)
def test_missing_binary(
    mock_exists,
    mock_run,
) -> None:
    """Missing binary should raise."""

    mock_run.side_effect = FileNotFoundError()

    backend = PiperTextToSpeech(
        executable="piper",
        model_path="voice.onnx",
    )

    with pytest.raises(TextToSpeechError):
        backend.speak("Hello")
