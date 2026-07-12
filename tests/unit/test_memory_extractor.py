"""
Unit tests for the MemoryExtractor.
"""

from __future__ import annotations

from ai.memory_extractor import MemoryExtractor
from ai.memory_importance import MemoryImportance
from ai.memory_type import MemoryType


class TestMemoryExtractor:
    """
    Tests for the MemoryExtractor.
    """

    def test_empty_message_returns_none(self) -> None:
        """
        Verify empty messages are ignored.
        """
        extractor = MemoryExtractor()

        memory = extractor.extract("")

        assert memory is None

    def test_whitespace_message_returns_none(self) -> None:
        """
        Verify whitespace-only messages are ignored.
        """
        extractor = MemoryExtractor()

        memory = extractor.extract("     ")

        assert memory is None

    def test_extract_user_memory(self) -> None:
        """
        Verify user identity memories are extracted.
        """
        extractor = MemoryExtractor()

        memory = extractor.extract(
            "My name is John"
        )

        assert memory is not None
        assert memory.content == "My name is John"
        assert memory.memory_type is MemoryType.USER
        assert memory.importance is MemoryImportance.CRITICAL

    def test_extract_preference_memory(self) -> None:
        """
        Verify preference memories are extracted.
        """
        extractor = MemoryExtractor()

        memory = extractor.extract(
            "I like Python"
        )

        assert memory is not None
        assert memory.memory_type is MemoryType.PREFERENCE
        assert memory.importance is MemoryImportance.HIGH

    def test_extract_fact_memory(self) -> None:
        """
        Verify fact memories are extracted.
        """
        extractor = MemoryExtractor()

        memory = extractor.extract(
            "Remember that Paris is the capital of France"
        )

        assert memory is not None
        assert memory.memory_type is MemoryType.FACT
        assert memory.importance is MemoryImportance.MEDIUM

    def test_non_memory_message_returns_none(self) -> None:
        """
        Verify ordinary conversation is ignored.
        """
        extractor = MemoryExtractor()

        memory = extractor.extract(
            "Hello, how are you?"
        )

        assert memory is None

    def test_generated_memory_has_identifier(self) -> None:
        """
        Verify generated memories have a unique identifier.
        """
        extractor = MemoryExtractor()

        memory = extractor.extract(
            "I like Python"
        )

        assert memory is not None
        assert memory.id != ""

    def test_generated_memory_metadata_defaults(self) -> None:
        """
        Verify generated memories have empty metadata.
        """
        extractor = MemoryExtractor()

        memory = extractor.extract(
            "I like Python"
        )

        assert memory is not None
        assert memory.metadata == {}

    def test_generated_memory_access_count_defaults(self) -> None:
        """
        Verify generated memories start with zero accesses.
        """
        extractor = MemoryExtractor()

        memory = extractor.extract(
            "I like Python"
        )

        assert memory is not None
        assert memory.access_count == 0

    def test_generated_memory_timestamps_match(self) -> None:
        """
        Verify generated timestamps are initialized consistently.
        """
        extractor = MemoryExtractor()

        memory = extractor.extract(
            "I like Python"
        )

        assert memory is not None
        assert memory.created_at == memory.updated_at
        assert memory.created_at == memory.last_accessed

    def test_detection_is_case_insensitive(self) -> None:
        """
        Verify extraction is case-insensitive.
        """
        extractor = MemoryExtractor()

        memory = extractor.extract(
            "i LIKE Python"
        )

        assert memory is not None
        assert memory.memory_type is MemoryType.PREFERENCE

    def test_extract_remember_statement(self) -> None:
        """
        Verify explicit remember statements are extracted.
        """
        extractor = MemoryExtractor()

        memory = extractor.extract(
            "remember milk tomorrow"
        )

        assert memory is not None
        assert memory.memory_type is MemoryType.FACT
