"""
Unit tests for the MemoryResult model.
"""

from __future__ import annotations

from datetime import datetime

from ai.memory_importance import MemoryImportance
from ai.memory_record import MemoryRecord
from ai.memory_result import MemoryResult
from ai.memory_type import MemoryType


class TestMemoryResult:
    """
    Tests for the MemoryResult model.
    """

    @staticmethod
    def create_memory(memory_id: str, content: str) -> MemoryRecord:
        """
        Create a memory record for testing.

        Args:
            memory_id: Unique memory identifier.
            content: Memory content.

        Returns:
            A populated memory record.
        """
        now = datetime.now()

        return MemoryRecord(
            id=memory_id,
            content=content,
            memory_type=MemoryType.FACT,
            importance=MemoryImportance.MEDIUM,
            created_at=now,
            updated_at=now,
            last_accessed=now,
        )

    def test_default_result(self) -> None:
        """
        Verify the default memory result.
        """
        result = MemoryResult()

        assert result.memories == []
        assert result.total_matches == 0
        assert result.returned_count == 0
        assert result.truncated is False

    def test_result_with_memories(self) -> None:
        """
        Verify a populated memory result.
        """
        memories = [
            self.create_memory("1", "Python"),
            self.create_memory("2", "SQLite"),
        ]

        result = MemoryResult(
            memories=memories,
            total_matches=2,
            returned_count=2,
            truncated=False,
        )

        assert result.memories == memories
        assert result.total_matches == 2
        assert result.returned_count == 2
        assert result.truncated is False

    def test_truncated_result(self) -> None:
        """
        Verify a truncated search result.
        """
        memories = [
            self.create_memory("1", "Memory"),
        ]

        result = MemoryResult(
            memories=memories,
            total_matches=10,
            returned_count=1,
            truncated=True,
        )

        assert result.total_matches == 10
        assert result.returned_count == 1
        assert result.truncated is True

    def test_empty_memory_list(self) -> None:
        """
        Verify an empty result.
        """
        result = MemoryResult(
            memories=[],
            total_matches=0,
            returned_count=0,
            truncated=False,
        )

        assert len(result.memories) == 0

    def test_returned_count_matches_memories(self) -> None:
        """
        Verify the returned count matches the number of memories.
        """
        memories = [
            self.create_memory("1", "One"),
            self.create_memory("2", "Two"),
            self.create_memory("3", "Three"),
        ]

        result = MemoryResult(
            memories=memories,
            total_matches=3,
            returned_count=len(memories),
            truncated=False,
        )

        assert result.returned_count == len(result.memories)
