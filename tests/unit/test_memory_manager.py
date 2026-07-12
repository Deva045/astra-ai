"""Unit tests for the MemoryManager."""

from __future__ import annotations

from datetime import datetime

from ai.memory_importance import MemoryImportance
from ai.memory_manager import MemoryManager
from ai.memory_query import MemoryQuery
from ai.memory_record import MemoryRecord
from ai.memory_repository import MemoryRepository
from ai.memory_result import MemoryResult
from ai.memory_type import MemoryType


class FakeMemoryRepository(MemoryRepository):
    """Simple in-memory repository used for testing."""

    def __init__(self) -> None:
        self._memories: dict[str, MemoryRecord] = {}

    def add(self, memory: MemoryRecord) -> None:
        self._memories[memory.id] = memory

    def get(self, memory_id: str) -> MemoryRecord | None:
        return self._memories.get(memory_id)

    def update(self, memory: MemoryRecord) -> None:
        self._memories[memory.id] = memory

    def delete(self, memory_id: str) -> None:
        self._memories.pop(memory_id, None)

    def search(self, query: MemoryQuery) -> MemoryResult:
        memories = list(self._memories.values())

        if query.text:
            memories = [
                memory
                for memory in memories
                if query.text.lower() in memory.content.lower()
            ]

        if query.memory_types:
            memories = [
                memory
                for memory in memories
                if memory.memory_type in query.memory_types
            ]

        memories = memories[: query.limit]

        return MemoryResult(
            memories=memories,
            total_matches=len(memories),
            returned_count=len(memories),
            truncated=False,
        )

    def list_all(self) -> list[MemoryRecord]:
        return list(self._memories.values())

    def clear(self) -> None:
        self._memories.clear()

    def count(self) -> int:
        return len(self._memories)


def create_memory(
    memory_id: str,
    content: str,
) -> MemoryRecord:
    """Create a memory for testing."""

    now = datetime.now()

    return MemoryRecord(
        id=memory_id,
        content=content,
        memory_type=MemoryType.FACT,
        importance=MemoryImportance.MEDIUM,
        created_at=now,
        updated_at=now,
        last_accessed=now,
        access_count=0,
        metadata={},
    )


def create_manager() -> MemoryManager:
    """Create a memory manager with a fake repository."""
    return MemoryManager(FakeMemoryRepository())


def test_add_memory() -> None:
    """Memory should be stored."""

    manager = create_manager()

    memory = create_memory("1", "Python")

    manager.add_memory(memory)

    assert manager.memory_count() == 1


def test_get_memory() -> None:
    """Stored memory should be retrievable."""

    manager = create_manager()

    memory = create_memory("1", "Python")

    manager.add_memory(memory)

    retrieved = manager.get_memory("1")

    assert retrieved is not None
    assert retrieved.id == "1"
    assert retrieved.content == "Python"


def test_get_missing_memory() -> None:
    """Unknown memories should return None."""

    manager = create_manager()

    assert manager.get_memory("missing") is None


def test_update_memory() -> None:
    """Updated memory should be returned."""

    manager = create_manager()

    memory = create_memory("1", "Old")

    manager.add_memory(memory)

    memory.content = "New"

    manager.update_memory(memory)

    updated = manager.get_memory("1")

    assert updated is not None
    assert updated.content == "New"


def test_delete_memory() -> None:
    """Deleted memory should no longer exist."""

    manager = create_manager()

    manager.add_memory(create_memory("1", "Delete"))

    manager.delete_memory("1")

    assert manager.get_memory("1") is None
    assert manager.memory_count() == 0


def test_list_memories() -> None:
    """All memories should be returned."""

    manager = create_manager()

    manager.add_memory(create_memory("1", "One"))
    manager.add_memory(create_memory("2", "Two"))

    memories = manager.list_memories()

    assert len(memories) == 2


def test_search_memories() -> None:
    """Search should delegate to the repository."""

    manager = create_manager()

    manager.add_memory(create_memory("1", "Python"))
    manager.add_memory(create_memory("2", "Java"))

    result = manager.search_memories(
        MemoryQuery(text="Python")
    )

    assert result.returned_count == 1
    assert result.memories[0].content == "Python"


def test_clear_memories() -> None:
    """All memories should be removed."""

    manager = create_manager()

    manager.add_memory(create_memory("1", "One"))
    manager.add_memory(create_memory("2", "Two"))

    manager.clear_memories()

    assert manager.memory_count() == 0
    assert manager.list_memories() == []


def test_memory_count() -> None:
    """The memory count should be correct."""

    manager = create_manager()

    assert manager.memory_count() == 0

    manager.add_memory(create_memory("1", "One"))
    manager.add_memory(create_memory("2", "Two"))
    manager.add_memory(create_memory("3", "Three"))

    assert manager.memory_count() == 3
