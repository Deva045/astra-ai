"""
Unit tests for the MemoryRecord model.
"""

from __future__ import annotations

from datetime import datetime

from ai.memory_importance import MemoryImportance
from ai.memory_record import MemoryRecord
from ai.memory_type import MemoryType


class TestMemoryRecord:
    """
    Tests for the MemoryRecord model.
    """

    def test_create_memory_record(self) -> None:
        """
        Verify a memory record can be created.
        """
        now = datetime.now()

        memory = MemoryRecord(
            id="memory-1",
            content="Python is a programming language.",
            memory_type=MemoryType.FACT,
            importance=MemoryImportance.MEDIUM,
            created_at=now,
            updated_at=now,
            last_accessed=now,
        )

        assert memory.id == "memory-1"
        assert memory.content == "Python is a programming language."
        assert memory.memory_type is MemoryType.FACT
        assert memory.importance is MemoryImportance.MEDIUM
        assert memory.created_at == now
        assert memory.updated_at == now
        assert memory.last_accessed == now
        assert memory.access_count == 0
        assert memory.metadata == {}

    def test_custom_access_count(self) -> None:
        """
        Verify a custom access count is stored.
        """
        now = datetime.now()

        memory = MemoryRecord(
            id="memory-2",
            content="Important memory",
            memory_type=MemoryType.LONG_TERM,
            importance=MemoryImportance.HIGH,
            created_at=now,
            updated_at=now,
            last_accessed=now,
            access_count=5,
        )

        assert memory.access_count == 5

    def test_custom_metadata(self) -> None:
        """
        Verify metadata is stored.
        """
        now = datetime.now()

        metadata = {
            "source": "conversation",
            "topic": "python",
        }

        memory = MemoryRecord(
            id="memory-3",
            content="Metadata test",
            memory_type=MemoryType.CONVERSATION,
            importance=MemoryImportance.LOW,
            created_at=now,
            updated_at=now,
            last_accessed=now,
            metadata=metadata,
        )

        assert memory.metadata == metadata

    def test_default_metadata_is_empty(self) -> None:
        """
        Verify metadata defaults to an empty dictionary.
        """
        now = datetime.now()

        memory = MemoryRecord(
            id="memory-4",
            content="Default metadata",
            memory_type=MemoryType.USER,
            importance=MemoryImportance.MEDIUM,
            created_at=now,
            updated_at=now,
            last_accessed=now,
        )

        assert memory.metadata == {}

    def test_default_access_count_is_zero(self) -> None:
        """
        Verify the default access count.
        """
        now = datetime.now()

        memory = MemoryRecord(
            id="memory-5",
            content="Access count",
            memory_type=MemoryType.SYSTEM,
            importance=MemoryImportance.CRITICAL,
            created_at=now,
            updated_at=now,
            last_accessed=now,
        )

        assert memory.access_count == 0
