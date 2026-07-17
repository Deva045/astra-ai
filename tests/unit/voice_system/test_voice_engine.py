"""
Unit tests for the VoiceEngine.
"""

from __future__ import annotations

import pytest

from voice.assistant import VoiceAssistant
from voice.audio_manager import AudioManager
from voice.interfaces import AudioInput, SpeechToText, TextToSpeech, WakeWordDetector
from voice.microphone_manager import MicrophoneManager
from voice.models import AudioChunk, VoiceState
from voice.speech_to_text import SpeechToTextManager
from voice.text_to_speech import TextToSpeechManager
from voice.voice_engine import VoiceEngine
from voice.wake_word import WakeWordManager


class DummyAudioInput(AudioInput):
    """Mock microphone backend."""

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
    """Mock STT backend."""

    def transcribe(self, audio: AudioChunk) -> str:
        return "Hello Nexus"


class DummyTextToSpeech(TextToSpeech):
    """Mock TTS backend."""

    def __init__(self) -> None:
        self.last_text: str | None = None

    def speak(self, text: str) -> None:
        self.last_text = text


class DummyWakeWordDetector(WakeWordDetector):
    """Mock wake-word detector."""

    def __init__(self) -> None:
        self.detected_value = True

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def detected(self) -> bool:
        return self.detected_value


class DummyAssistant(VoiceAssistant):
    """Mock AI assistant."""

    def process_text(self, text: str) -> str:
        return f"AI: {text}"


def create_engine() -> tuple[VoiceEngine, DummyTextToSpeech]:
    """
    Create a fully configured VoiceEngine.
    """
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
        DummyWakeWordDetector(),
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

    return engine, tts_backend


def test_initial_state() -> None:
    """Engine should start idle."""
    engine, _ = create_engine()

    assert engine.state is VoiceState.IDLE


def test_start() -> None:
    """Starting should leave the engine idle."""
    engine, _ = create_engine()

    engine.start()

    assert engine.state is VoiceState.IDLE


def test_stop() -> None:
    """Stopping should leave the engine idle."""
    engine, _ = create_engine()

    engine.start()
    engine.stop()

    assert engine.state is VoiceState.IDLE


def test_listen_once() -> None:
    """Audio should be transcribed."""
    engine, _ = create_engine()

    text = engine.listen_once()

    assert text == "Hello Nexus"


def test_speak() -> None:
    """Speech should be delegated to the TTS backend."""
    engine, backend = create_engine()

    engine.speak("Testing")

    assert backend.last_text == "Testing"


def test_process_once() -> None:
    """Wake-word detection should trigger transcription."""
    engine, _ = create_engine()

    engine.start()

    assert engine.process_once() == "Hello Nexus"


def test_chat_once() -> None:
    """Complete voice interaction should succeed."""
    engine, backend = create_engine()

    engine.start()

    response = engine.chat_once()

    assert response == "AI: Hello Nexus"
    assert backend.last_text == "AI: Hello Nexus"


def test_reset() -> None:
    """Reset should restore idle state."""
    engine, _ = create_engine()

    engine.start()
    engine.reset()

    assert engine.state is VoiceState.IDLE


def test_multiple_interactions() -> None:
    """Engine should support repeated interactions."""
    engine, _ = create_engine()

    engine.start()

    assert engine.chat_once() == "AI: Hello Nexus"
    assert engine.chat_once() == "AI: Hello Nexus"


def test_no_wake_word() -> None:
    """No response should be generated if wake word is absent."""

    class NoWakeWord(WakeWordDetector):
        def start(self) -> None:
            pass

        def stop(self) -> None:
            pass

        def detected(self) -> bool:
            return False

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
        NoWakeWord(),
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

    engine.start()

    assert engine.chat_once() is None
