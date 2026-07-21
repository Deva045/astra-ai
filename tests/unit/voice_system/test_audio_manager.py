"""
Unit tests for the AudioManager.
"""

from __future__ import annotations

import pytest

from voice.audio_manager import AudioManager
from voice.exceptions import AudioError
from voice.models import VoiceSettings


def test_default_settings() -> None:
    """AudioManager should initialize with default settings."""
    manager = AudioManager()

    settings = manager.settings

    assert settings.sample_rate == 16000
    assert settings.channels == 1
    assert settings.chunk_size == 1024
    assert settings.wake_word_enabled is True


def test_custom_settings() -> None:
    """AudioManager should accept valid custom settings."""
    settings = VoiceSettings(
        sample_rate=44100,
        channels=2,
        chunk_size=2048,
    )

    manager = AudioManager(settings)

    assert manager.settings.sample_rate == 44100
    assert manager.settings.channels == 2
    assert manager.settings.chunk_size == 2048


def test_update_settings() -> None:
    """Updating settings should replace the current configuration."""
    manager = AudioManager()

    settings = VoiceSettings(
        sample_rate=22050,
        channels=1,
        chunk_size=512,
    )

    manager.update_settings(settings)

    assert manager.settings.sample_rate == 22050
    assert manager.settings.chunk_size == 512


def test_set_input_device() -> None:
    """Input device should be stored correctly."""
    manager = AudioManager()

    manager.set_input_device("Microphone")

    assert manager.get_input_device() == "Microphone"


def test_set_output_device() -> None:
    """Output device should be stored correctly."""
    manager = AudioManager()

    manager.set_output_device("Speaker")

    assert manager.get_output_device() == "Speaker"


@pytest.mark.parametrize(
    "sample_rate",
    [
        0,
        4000,
        96000,
    ],
)
def test_invalid_sample_rate(sample_rate: int) -> None:
    """Invalid sample rates should raise AudioError."""
    settings = VoiceSettings(sample_rate=sample_rate)

    with pytest.raises(AudioError):
        AudioManager(settings)


@pytest.mark.parametrize(
    "channels",
    [
        0,
        3,
        10,
    ],
)
def test_invalid_channels(channels: int) -> None:
    """Invalid channel counts should raise AudioError."""
    settings = VoiceSettings(channels=channels)

    with pytest.raises(AudioError):
        AudioManager(settings)


@pytest.mark.parametrize(
    "chunk_size",
    [
        0,
        64,
        16384,
    ],
)
def test_invalid_chunk_size(chunk_size: int) -> None:
    """Invalid chunk sizes should raise AudioError."""
    settings = VoiceSettings(chunk_size=chunk_size)

    with pytest.raises(AudioError):
        AudioManager(settings)


def test_invalid_speech_timeout() -> None:
    """Speech timeout must be positive."""
    settings = VoiceSettings(
        speech_timeout=0,
    )

    with pytest.raises(AudioError):
        AudioManager(settings)


def test_invalid_silence_timeout() -> None:
    """Silence timeout must be positive."""
    settings = VoiceSettings(
        silence_timeout=-1,
    )

    with pytest.raises(AudioError):
        AudioManager(settings)


def test_reset() -> None:
    """Reset should restore default settings."""
    manager = AudioManager()

    manager.set_input_device("Mic")
    manager.set_output_device("Speaker")

    manager.reset()

    settings = manager.settings

    assert settings.sample_rate == 16000
    assert settings.channels == 1
    assert settings.chunk_size == 1024
    assert manager.get_input_device() is None
    assert manager.get_output_device() is None


def test_supports_streaming() -> None:
    """Streaming is not implemented yet."""
    manager = AudioManager()

    assert manager.supports_streaming() is False
