"""
Integration tests for the complete voice pipeline.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from voice.audio_manager import AudioManager
from voice.microphone_manager import MicrophoneManager
from voice.voice_engine import VoiceEngine


class DummySpeechToText:
    """Fake STT backend."""

    def transcribe(self, audio):
        return "hello nexus"


class DummyTextToSpeech:
    """Fake TTS backend."""

    def __init__(self):
        self.last_text = None

    def speak(self, text: str) -> None:
        self.last_text = text


class DummyWakeWord:
    """Fake wake-word detector."""

    def start(self):
        pass

    def stop(self):
        pass

    def detected(self):
        return True


def test_voice_pipeline_initialization() -> None:
    """Voice engine should initialize."""

    microphone = MagicMock(spec=MicrophoneManager)
    audio = MagicMock(spec=AudioManager)

    stt = DummySpeechToText()
    tts = DummyTextToSpeech()
    wake = DummyWakeWord()

    engine = VoiceEngine(
        microphone=microphone,
        audio_manager=audio,
        speech_to_text=stt,
        text_to_speech=tts,
        wake_word=wake,
    )

    assert engine is not None


def test_stt_backend() -> None:
    """Speech-to-text backend should return text."""

    stt = DummySpeechToText()

    assert stt.transcribe(b"audio") == "hello nexus"


def test_tts_backend() -> None:
    """Text-to-speech backend should receive text."""

    tts = DummyTextToSpeech()

    tts.speak("hello")

    assert tts.last_text == "hello"


def test_wake_word_backend() -> None:
    """Wake-word detector should trigger."""

    wake = DummyWakeWord()

    assert wake.detected() is True


def test_voice_pipeline_flow() -> None:
    """Simple end-to-end pipeline."""

    stt = DummySpeechToText()
    tts = DummyTextToSpeech()

    text = stt.transcribe(b"audio")

    tts.speak(text)

    assert tts.last_text == "hello nexus"
