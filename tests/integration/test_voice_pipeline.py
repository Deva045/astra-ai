"""
Integration tests for the complete voice pipeline.
"""

from __future__ import annotations

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
        self.last_text: str | None = None

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


def create_engine():
    """Create a fully configured voice engine."""

    audio_manager = AudioManager()

    microphone = MicrophoneManager(
        audio_manager,
        DummyAudioInput(),
    )

    stt = SpeechToTextManager(
        DummySpeechToText(),
    )

    tts_backend = DummyTextToSpeech()

    tts = TextToSpeechManager(
        tts_backend,
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

    return (
        engine,
        stt,
        tts,
        tts_backend,
        wake,
        assistant,
    )


def test_voice_pipeline_initialization() -> None:
    """Voice engine should initialize."""

    engine, *_ = create_engine()

    assert engine is not None


def test_stt_backend() -> None:
    """Speech-to-text backend should return text."""

    _, stt, _, _, _, _ = create_engine()

    audio = AudioChunk(
        data=b"audio",
        sample_rate=16000,
        channels=1,
        sample_width=2,
    )

    assert stt.transcribe(audio) == "hello nexus"


def test_tts_backend() -> None:
    """Text-to-speech backend should receive text."""

    _, _, tts, tts_backend, _, _ = create_engine()

    tts.speak("hello")

    assert tts_backend.last_text == "hello"


def test_wake_word_backend() -> None:
    """Wake-word detector should trigger."""

    _, _, _, _, wake, _ = create_engine()

    wake.start()

    assert wake.detect() is True

    wake.stop()


def test_voice_pipeline_flow() -> None:
    """Simple end-to-end pipeline."""

    (
        engine,
        _,
        _,
        tts_backend,
        wake,
        _,
    ) = create_engine()

    wake.start()

    response = engine.chat_once()

    wake.stop()

    assert response == "AI Response: hello nexus"
    assert tts_backend.last_text == "AI Response: hello nexus"
