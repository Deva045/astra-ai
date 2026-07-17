"""
Integration tests for Voice ↔ Memory interaction.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from voice.audio_manager import AudioManager
from voice.microphone_manager import MicrophoneManager
from voice.voice_engine import VoiceEngine


class DummySpeechToText:
    """Fake Speech-to-Text backend."""

    def transcribe(self, audio):
        return "remember my favorite color is blue"


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


class DummyMemory:
    """Simple in-memory store used for testing."""

    def __init__(self):
        self.storage: list[str] = []

    def save(self, text: str) -> None:
        self.storage.append(text)

    def search(self, query: str):
        return [
            item
            for item in self.storage
            if query.lower() in item.lower()
        ]


@pytest.fixture
def voice_engine():
    """Create a mocked voice engine."""

    microphone = MagicMock(spec=MicrophoneManager)
    audio_manager = MagicMock(spec=AudioManager)

    stt = DummySpeechToText()
    tts = DummyTextToSpeech()
    wake = DummyWakeWord()

    engine = VoiceEngine(
        microphone=microphone,
        audio_manager=audio_manager,
        speech_to_text=stt,
        text_to_speech=tts,
        wake_word=wake,
    )

    return engine, stt, tts


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


def test_voice_to_memory():
    """Speech should be saved into memory."""

    _, stt, _ = voice_engine()

    memory = DummyMemory()

    text = stt.transcribe(b"audio")

    memory.save(text)

    assert memory.storage[0] == "remember my favorite color is blue"


def test_memory_to_tts():
    """Memory retrieval should be spoken."""

    _, _, tts = voice_engine()

    memory = DummyMemory()

    memory.save("favorite color is blue")

    result = memory.search("color")[0]

    tts.speak(result)

    assert tts.last_text == "favorite color is blue"


def test_complete_voice_memory_flow():
    """Voice → Memory → TTS integration."""

    _, stt, tts = voice_engine()

    memory = DummyMemory()

    speech = stt.transcribe(b"audio")

    memory.save(speech)

    result = memory.search("favorite")[0]

    tts.speak(result)

    assert (
        tts.last_text
        == "remember my favorite color is blue"
    )
