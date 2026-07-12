"""
Integration tests for the Nexus AI memory system.
"""

from __future__ import annotations

from datetime import datetime

from ai.memory_importance import MemoryImportance
from ai.memory_manager import MemoryManager
from ai.memory_query import MemoryQuery
from ai.memory_record import MemoryRecord
from ai.memory_type import MemoryType
from ai.sqlite_memory_repository import SQLiteMemoryRepository
from database.sqlite_database import SQLiteDatabase


class TestMemoryIntegration:
    """
    Integration tests for the memory system.
    """

    def create_manager(self) -> MemoryManager:
        """
        Create a fresh memory manager backed by an in-memory database.
        """

        database = SQLiteDatabase(":memory:")
        repository = SQLiteMemoryRepository(database)

        return MemoryManager(repository)

    def create_memory(
        self,
        memory_id: str,
        content: str,
        memory_type: MemoryType = MemoryType.FACT,
        importance: MemoryImportance = MemoryImportance.MEDIUM,
    ) -> MemoryRecord:
        """
        Create a memory record.
        """

        now = datetime.now()

        return MemoryRecord(
            id=memory_id,
            content=content,
            memory_type=memory_type,
            importance=importance,
            created_at=now,
            updated_at=now,
            last_accessed=now,
        )

    def test_add_and_get_memory(self) -> None:
        """
        Verify a stored memory can be retrieved.
        """

        manager = self.create_manager()

        memory = self.create_memory(
            "1",
            "Python is awesome",
        )

        manager.add_memory(memory)

        retrieved = manager.get_memory("1")

        assert retrieved is not None
        assert retrieved.id == "1"
        assert retrieved.content == "Python is awesome"

    def test_memory_count(self) -> None:
        """
        Verify memory counting.
        """

        manager = self.create_manager()

        assert manager.memory_count() == 0

        manager.add_memory(
            self.create_memory(
                "1",
                "Memory One",
            )
        )

        manager.add_memory(
            self.create_memory(
                "2",
                "Memory Two",
            )
        )

        assert manager.memory_count() == 2

    def test_search_memory(self) -> None:
        """
        Verify searching memories.
        """

        manager = self.create_manager()

        manager.add_memory(
            self.create_memory(
                "1",
                "I like Python",
            )
        )

        manager.add_memory(
            self.create_memory(
                "2",
                "I like Java",
            )
        )

        result = manager.search_memories(
            MemoryQuery(
                text="Python",
            )
        )

        assert result.returned_count == 1
        assert result.memories[0].content == "I like Python"

    def test_delete_memory(self) -> None:
        """
        Verify deleting memories.
        """

        manager = self.create_manager()

        manager.add_memory(
            self.create_memory(
                "1",
                "Delete me",
            )
        )

        assert manager.memory_count() == 1

        manager.delete_memory("1")

        assert manager.memory_count() == 0

    def test_clear_memories(self) -> None:
        """
        Verify clearing all memories.
        """

        manager = self.create_manager()

        manager.add_memory(
            self.create_memory(
                "1",
                "A",
            )
        )

        manager.add_memory(
            self.create_memory(
                "2",
                "B",
            )
        )

        assert manager.memory_count() == 2

        manager.clear_memories()

        assert manager.memory_count() == 0

    def test_update_memory(self) -> None:
        """
        Verify updating an existing memory.
        """

        manager = self.create_manager()

        memory = self.create_memory(
            "1",
            "Old Content",
        )

        manager.add_memory(memory)

        memory.content = "New Content"

        manager.update_memory(memory)

        updated = manager.get_memory("1")

        assert updated is not None
        assert updated.content == "New Content"

    def test_list_memories(self) -> None:
        """
        Verify listing all memories.
        """

        manager = self.create_manager()

        manager.add_memory(
            self.create_memory(
                "1",
                "First",
            )
        )

        manager.add_memory(
            self.create_memory(
                "2",
                "Second",
            )
        )

        memories = manager.list_memories()

        assert len(memories) == 2

    def test_search_by_memory_type(self) -> None:
        """
        Verify filtering by memory type.
        """

        manager = self.create_manager()

        manager.add_memory(
            self.create_memory(
                "1",
                "User Memory",
                memory_type=MemoryType.USER,
            )
        )

        manager.add_memory(
            self.create_memory(
                "2",
                "Fact Memory",
                memory_type=MemoryType.FACT,
            )
        )

        result = manager.search_memories(
            MemoryQuery(
                memory_types=[
                    MemoryType.USER,
                ]
            )
        )

        assert result.returned_count == 1
        assert result.memories[0].memory_type == MemoryType.USER
