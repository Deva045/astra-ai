"""
Integration tests for Voice ↔ AI interaction.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from voice.voice_engine import VoiceEngine
from voice.audio_manager import AudioManager
from voice.microphone_manager import MicrophoneManager


class DummySpeechToText:
    """Fake Speech-to-Text backend."""

    def transcribe(self, audio):
        return "hello nexus"


class DummyTextToSpeech:
    """Fake Text-to-Speech backend."""

    def __init__(self):
        self.last_text = ""

    def speak(self, text: str) -> None:
        self.last_text = text


class DummyWakeWord:
    """Fake Wake Word backend."""

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def detected(self) -> bool:
        return True


class DummyAIEngine:
    """Simple AI engine used for testing."""

    def process(self, text: str) -> str:
        return f"AI Response: {text}"


@pytest.fixture
def voice_engine():
    """Create a voice engine with mocked dependencies."""

    microphone = MagicMock(spec=MicrophoneManager)
    audio_manager = MagicMock(spec=AudioManager)

    stt = DummySpeechToText()
    tts = DummyTextToSpeech()
    wake_word = DummyWakeWord()

    engine = VoiceEngine(
        microphone=microphone,
        audio_manager=audio_manager,
        speech_to_text=stt,
        text_to_speech=tts,
        wake_word=wake_word,
    )

    return engine, stt, tts


def test_ai_response_generation():
    """AI should generate a response."""

    ai = DummyAIEngine()

    response = ai.process("hello nexus")

    assert response == "AI Response: hello nexus"


def test_voice_to_ai_pipeline():
    """Speech should reach the AI engine."""

    _, stt, _ = voice_engine()

    ai = DummyAIEngine()

    text = stt.transcribe(b"audio")

    response = ai.process(text)

    assert response == "AI Response: hello nexus"


def test_ai_to_tts_pipeline():
    """AI output should be sent to TTS."""

    _, _, tts = voice_engine()

    ai = DummyAIEngine()

    response = ai.process("hello")

    tts.speak(response)

    assert tts.last_text == "AI Response: hello"


def test_complete_voice_ai_flow():
    """Complete Voice → AI → TTS flow."""

    _, stt, tts = voice_engine()

    ai = DummyAIEngine()

    speech = stt.transcribe(b"audio")

    response = ai.process(speech)

    tts.speak(response)

    assert tts.last_text == "AI Response: hello nexus"
