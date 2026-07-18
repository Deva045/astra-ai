"""
Integration tests for Voice ↔ Memory interaction.
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
        return "remember my favorite color is blue"


class DummyTextToSpeech(TextToSpeech):
    """Fake TTS backend."""

    def __init__(self) -> None:
        self.last_text = ""

    def speak(self, text: str) -> None:
        self.last_text = text


class DummyWakeWord(WakeWordDetector):
    """Fake wake-word backend."""

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def detected(self) -> bool:
        return True


class DummyAssistant(VoiceAssistant):
    """Dummy assistant."""

    def process_text(self, text: str) -> str:
        return text


class DummyMemory:
    """Simple in-memory store."""

    def __init__(self) -> None:
        self.storage: list[str] = []

    def save(self, text: str) -> None:
        self.storage.append(text)

    def search(self, query: str) -> list[str]:
        return [
            item
            for item in self.storage
            if query.lower() in item.lower()
        ]


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


def test_memory_store():
    """Memory should store conversations."""

    memory = DummyMemory()

    memory.save("remember my favorite color is blue")

    assert len(memory.storage) == 1


def test_memory_search():
    """Memory should return matching entries."""

    memory = DummyMemory()

    memory.save("favorite color is blue")
    memory.save("favorite food is pizza")

    results = memory.search("color")

    assert len(results) == 1
    assert results[0] == "favorite color is blue"


def test_voice_to_memory(voice_engine):
    """Speech should be saved into memory."""

    engine, _, _, wake = voice_engine

    memory = DummyMemory()

    wake.start()

    speech = engine.process_once()

    wake.stop()

    assert speech is not None

    memory.save(speech)

    assert memory.storage[0] == "remember my favorite color is blue"


def test_memory_to_tts(voice_engine):
    """Memory retrieval should be spoken."""

    _, _, tts, _ = voice_engine

    memory = DummyMemory()

    memory.save("favorite color is blue")

    result = memory.search("color")[0]

    tts.speak(result)

    assert tts.backend.last_text == "favorite color is blue"


def test_complete_voice_memory_flow(voice_engine):
    """Voice → Memory → TTS integration."""

    engine, _, tts, wake = voice_engine

    memory = DummyMemory()

    wake.start()

    speech = engine.process_once()

    wake.stop()

    assert speech is not None

    memory.save(speech)

    result = memory.search("favorite")[0]

    tts.speak(result)

    assert tts.backend.last_text == "remember my favorite color is blue"
