"""
Unit tests for the VoiceAssistant adapter.
"""

from __future__ import annotations

from collections.abc import Iterator

from voice.assistant import (
    AIEngineVoiceAssistant,
    VoiceAssistant,
)


class DummyAIEngine:
    """
    Simple AIEngine mock.
    """

    def chat(self, text: str) -> str:
        return f"Response: {text}"

    def stream_chat(self, text: str) -> Iterator[str]:
        yield "Response:"
        yield " "
        yield text


class DummyVoiceAssistant(VoiceAssistant):
    """
    Concrete VoiceAssistant used for testing.
    """

    def process_text(self, text: str) -> str:
        return f"Processed: {text}"


def test_voice_assistant_process_text() -> None:
    """
    VoiceAssistant should process text.
    """
    assistant = DummyVoiceAssistant()

    assert assistant.process_text("Hello") == "Processed: Hello"


def test_voice_assistant_stream_text() -> None:
    """
    Default stream_text() should yield process_text().
    """
    assistant = DummyVoiceAssistant()

    chunks = list(
        assistant.stream_text("Hello")
    )

    assert chunks == [
        "Processed: Hello",
    ]


def test_ai_engine_voice_assistant_process_text() -> None:
    """
    AIEngineVoiceAssistant should delegate to AIEngine.chat().
    """
    engine = DummyAIEngine()

    assistant = AIEngineVoiceAssistant(engine)

    response = assistant.process_text(
        "Hello Nexus"
    )

    assert response == "Response: Hello Nexus"


def test_ai_engine_voice_assistant_stream_text() -> None:
    """
    AIEngineVoiceAssistant should delegate
    to AIEngine.stream_chat().
    """
    engine = DummyAIEngine()

    assistant = AIEngineVoiceAssistant(engine)

    chunks = list(
        assistant.stream_text(
            "Hello Nexus"
        )
    )

    assert chunks == [
        "Response:",
        " ",
        "Hello Nexus",
    ]


def test_engine_property() -> None:
    """
    engine property should return
    the wrapped AIEngine.
    """
    engine = DummyAIEngine()

    assistant = AIEngineVoiceAssistant(
        engine
    )

    assert assistant.engine is engine
