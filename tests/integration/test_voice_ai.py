"""
Integration tests for Voice ↔ AI interaction.
"""

from __future__ import annotations

import pytest

from voice.assistant import VoiceAssistant
from voice.audio_manager import AudioManager
from voice.interfaces import (
    AudioInput,
    SpeechToText,
    TextToSpeech,
    WakeWordDetector,
)
from voice.microphone_manager import MicrophoneManager
from voice.models import AudioChunk
from voice.speech_to_text import SpeechToTextManager
from voice.text_to_speech import TextToSpeechManager
from voice.voice_engine import VoiceEngine
from voice.wake_word import WakeWordManager


class DummyAudioInput(AudioInput):
    """Fake microphone backend."""

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def read(self) -> AudioChunk:
        return AudioChunk(
            data=b"audio",
            sample_rate=16000,
            channels=1,
            sample_width=2,
        )


class DummySpeechToText(SpeechToText):
    """Fake STT backend."""

    def transcribe(self, audio: AudioChunk) -> str:
        return "hello nexus"


class DummyTextToSpeech(TextToSpeech):
    """Fake TTS backend."""

    def __init__(self) -> None:
        self.last_text = ""

    def speak(self, text: str) -> None:
        self.last_text = text


class DummyWakeWord(WakeWordDetector):
    """Fake wake-word detector."""

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def detected(self) -> bool:
        return True


class DummyAssistant(VoiceAssistant):
    """Fake AI assistant."""

    def process_text(self, text: str) -> str:
        return f"AI Response: {text}"


@pytest.fixture
def voice_engine():
    """Create a fully configured voice engine."""

    audio_manager = AudioManager()

    microphone = MicrophoneManager(
        audio_manager,
        DummyAudioInput(),
    )

    stt = SpeechToTextManager(
        DummySpeechToText(),
    )

    tts = TextToSpeechManager(
        DummyTextToSpeech(),
    )

    wake = WakeWordManager(
        DummyWakeWord(),
    )

    assistant = DummyAssistant()

    engine = VoiceEngine(
        audio_manager,
        microphone,
        stt,
        tts,
        wake,
        assistant,
    )

    return engine, stt, tts, wake


def test_ai_response_generation():
    """Assistant should generate a response."""

    assistant = DummyAssistant()

    response = assistant.process_text("hello nexus")

    assert response == "AI Response: hello nexus"


def test_voice_to_ai_pipeline(voice_engine):
    """Speech should reach the AI assistant."""

    engine, _, _, wake = voice_engine

    wake.start()

    response = engine.chat_once()

    wake.stop()

    assert response == "AI Response: hello nexus"


def test_ai_to_tts_pipeline(voice_engine):
    """AI output should be spoken."""

    engine, _, tts, wake = voice_engine

    wake.start()

    response = engine.chat_once()

    wake.stop()

    assert response == "AI Response: hello nexus"
    assert tts.backend.last_text == "AI Response: hello nexus"


def test_complete_voice_ai_flow(voice_engine):
    """Complete Voice → AI → TTS flow."""

    engine, _, tts, wake = voice_engine

    wake.start()

    response = engine.chat_once()

    wake.stop()

    assert response == "AI Response: hello nexus"
    assert tts.backend.last_text == "AI Response: hello nexus"
