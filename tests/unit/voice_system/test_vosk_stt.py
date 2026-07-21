"""
Unit tests for the VoskSpeechToText backend.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from voice.exceptions import SpeechToTextError
from voice.models import AudioChunk
from voice.backends.vosk_stt import VoskSpeechToText


def create_audio_chunk() -> AudioChunk:
    """Create dummy audio."""
    return AudioChunk(
        data=b"audio",
        sample_rate=16000,
        channels=1,
        sample_width=2,
    )


@patch("voice.backends.vosk_stt.Model")
@patch("voice.backends.vosk_stt.KaldiRecognizer")
@patch("voice.backends.vosk_stt.Path.exists", return_value=True)
def test_backend_initializes(
    mock_exists,
    mock_recognizer,
    mock_model,
) -> None:
    """Backend should initialize correctly."""

    backend = VoskSpeechToText("model")

    assert backend.sample_rate == 16000
    assert backend.model_path == Path("model")

    mock_model.assert_called_once()
    mock_recognizer.assert_called_once()


@patch("voice.backends.vosk_stt.Path.exists", return_value=False)
def test_missing_model(mock_exists) -> None:
    """Missing model should raise."""

    with pytest.raises(SpeechToTextError):
        VoskSpeechToText("missing-model")


@patch("voice.backends.vosk_stt.Model")
@patch("voice.backends.vosk_stt.KaldiRecognizer")
@patch("voice.backends.vosk_stt.Path.exists", return_value=True)
def test_transcribe(
    mock_exists,
    mock_recognizer,
    mock_model,
) -> None:
    """Audio should be transcribed."""

    recognizer = MagicMock()

    recognizer.AcceptWaveform.return_value = True
    recognizer.Result.return_value = (
        '{"text":"hello nexus"}'
    )

    mock_recognizer.return_value = recognizer

    backend = VoskSpeechToText("model")

    text = backend.transcribe(
        create_audio_chunk()
    )

    assert text == "hello nexus"


@patch("voice.backends.vosk_stt.Model")
@patch("voice.backends.vosk_stt.KaldiRecognizer")
@patch("voice.backends.vosk_stt.Path.exists", return_value=True)
def test_invalid_sample_rate(
    mock_exists,
    mock_recognizer,
    mock_model,
) -> None:
    """Wrong sample rate should raise."""

    backend = VoskSpeechToText("model")

    chunk = AudioChunk(
        data=b"audio",
        sample_rate=8000,
        channels=1,
        sample_width=2,
    )

    with pytest.raises(SpeechToTextError):
        backend.transcribe(chunk)


@patch("voice.backends.vosk_stt.Model")
@patch("voice.backends.vosk_stt.KaldiRecognizer")
@patch("voice.backends.vosk_stt.Path.exists", return_value=True)
def test_reset(
    mock_exists,
    mock_recognizer,
    mock_model,
) -> None:
    """Reset should recreate recognizer."""

    backend = VoskSpeechToText("model")

    backend.reset()

    assert mock_recognizer.call_count == 2
