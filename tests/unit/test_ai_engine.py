"""
Unit tests for the AI engine.
"""

from __future__ import annotations

from ai.engine import AIEngine
from ai.mock_llm import MockLLM


class TestAIEngine:
    """
    Tests for the AI engine.
    """

    def test_chat_returns_response(self) -> None:
        """
        Verify chat returns a response.
        """
        engine = AIEngine(
            llm=MockLLM(),
        )

        response = engine.chat("Hello")

        assert response
        assert "Nexus" in response

    def test_chat_adds_conversation_messages(self) -> None:
        """
        Verify chat stores the user and assistant messages.
        """
        engine = AIEngine(
            llm=MockLLM(),
        )

        engine.chat("Hello")

        assert engine.conversation.size() == 2

    def test_stream_chat_returns_chunks(self) -> None:
        """
        Verify streaming produces output.
        """
        engine = AIEngine(
            llm=MockLLM(),
        )

        chunks = list(
            engine.stream_chat("Hello")
        )

        assert len(chunks) > 0

    def test_stream_chat_adds_conversation_messages(self) -> None:
        """
        Verify streaming stores conversation history.
        """
        engine = AIEngine(
            llm=MockLLM(),
        )

        list(
            engine.stream_chat("Hello")
        )

        assert engine.conversation.size() == 2

    def test_preference_memory_is_stored(self) -> None:
        """
        Verify preference memories are stored.
        """
        engine = AIEngine(
            llm=MockLLM(),
        )

        initial = engine.memory_manager.memory_count()

        engine.chat("I like Python")

        assert (
            engine.memory_manager.memory_count()
            == initial + 1
        )

    def test_fact_memory_is_stored(self) -> None:
        """
        Verify fact memories are stored.
        """
        engine = AIEngine(
            llm=MockLLM(),
        )

        initial = engine.memory_manager.memory_count()

        engine.chat(
            "Remember that Paris is in France"
        )

        assert (
            engine.memory_manager.memory_count()
            == initial + 1
        )

    def test_normal_message_is_not_stored(self) -> None:
        """
        Verify ordinary conversation is not stored
        as long-term memory.
        """
        engine = AIEngine(
            llm=MockLLM(),
        )

        initial = engine.memory_manager.memory_count()

        engine.chat("Hello there!")

        assert (
            engine.memory_manager.memory_count()
            == initial
        )

    def test_multiple_chats_grow_history(self) -> None:
        """
        Verify conversation history grows correctly.
        """
        engine = AIEngine(
            llm=MockLLM(),
        )

        engine.chat("Hello")
        engine.chat("How are you?")

        assert engine.conversation.size() == 4
