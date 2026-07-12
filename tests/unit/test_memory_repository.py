"""Unit tests for the SQLiteMemoryRepository."""

from __future__ import annotations

from datetime import datetime

from ai.memory_importance import MemoryImportance
from ai.memory_query import MemoryQuery
from ai.memory_record import MemoryRecord
from ai.memory_type import MemoryType
from ai.sqlite_memory_repository import SQLiteMemoryRepository
from database.sqlite_database import SQLiteDatabase


def create_memory(
    memory_id: str,
    content: str,
    memory_type: MemoryType = MemoryType.FACT,
    importance: MemoryImportance = MemoryImportance.MEDIUM,
) -> MemoryRecord:
    """Create a test memory."""

    now = datetime.now()

    return MemoryRecord(
        id=memory_id,
        content=content,
        memory_type=memory_type,
        importance=importance,
        created_at=now,
        updated_at=now,
        last_accessed=now,
        access_count=0,
        metadata={},
    )


def create_repository() -> SQLiteMemoryRepository:
    """Create an in-memory repository."""

    database = SQLiteDatabase(":memory:")
    return SQLiteMemoryRepository(database)


def test_add_and_get_memory() -> None:
    """A stored memory can be retrieved."""

    repository = create_repository()

    memory = create_memory(
        "1",
        "Python is awesome",
    )

    repository.add(memory)

    retrieved = repository.get("1")

    assert retrieved is not None
    assert retrieved.id == memory.id
    assert retrieved.content == memory.content
    assert retrieved.memory_type == memory.memory_type
    assert retrieved.importance == memory.importance


def test_get_unknown_memory_returns_none() -> None:
    """Unknown IDs should return None."""

    repository = create_repository()

    assert repository.get("missing") is None


def test_update_memory() -> None:
    """Updating a memory should persist the changes."""

    repository = create_repository()

    memory = create_memory(
        "1",
        "Old content",
    )

    repository.add(memory)

    memory.content = "New content"

    repository.update(memory)

    updated = repository.get("1")

    assert updated is not None
    assert updated.content == "New content"


def test_delete_memory() -> None:
    """Deleting a memory removes it."""

    repository = create_repository()

    memory = create_memory(
        "1",
        "Delete me",
    )

    repository.add(memory)

    repository.delete("1")

    assert repository.get("1") is None


def test_count_memories() -> None:
    """Repository count should match stored memories."""

    repository = create_repository()

    assert repository.count() == 0

    repository.add(create_memory("1", "One"))
    repository.add(create_memory("2", "Two"))

    assert repository.count() == 2


def test_clear_repository() -> None:
    """Clearing removes every memory."""

    repository = create_repository()

    repository.add(create_memory("1", "One"))
    repository.add(create_memory("2", "Two"))

    assert repository.count() == 2

    repository.clear()

    assert repository.count() == 0
    assert repository.list_all() == []


def test_list_all_returns_all_memories() -> None:
    """list_all should return every stored memory."""

    repository = create_repository()

    repository.add(create_memory("1", "One"))
    repository.add(create_memory("2", "Two"))
    repository.add(create_memory("3", "Three"))

    memories = repository.list_all()

    assert len(memories) == 3


def test_search_by_text() -> None:
    """Search should filter by text."""

    repository = create_repository()

    repository.add(create_memory("1", "I like Python"))
    repository.add(create_memory("2", "I like Java"))

    result = repository.search(
        MemoryQuery(
            text="Python",
        )
    )

    assert result.total_matches == 1
    assert result.returned_count == 1
    assert result.memories[0].content == "I like Python"


def test_search_by_memory_type() -> None:
    """Search should filter by memory type."""

    repository = create_repository()

    repository.add(
        create_memory(
            "1",
            "User profile",
            memory_type=MemoryType.USER,
        )
    )

    repository.add(
        create_memory(
            "2",
            "Conversation",
            memory_type=MemoryType.CONVERSATION,
        )
    )

    result = repository.search(
        MemoryQuery(
            memory_types=[MemoryType.USER],
        )
    )

    assert result.total_matches == 1
    assert result.memories[0].memory_type == MemoryType.USER


def test_search_by_importance() -> None:
    """Search should filter by minimum importance."""

    repository = create_repository()

    repository.add(
        create_memory(
            "1",
            "Low",
            importance=MemoryImportance.LOW,
        )
    )

    repository.add(
        create_memory(
            "2",
            "Critical",
            importance=MemoryImportance.CRITICAL,
        )
    )

    result = repository.search(
        MemoryQuery(
            minimum_importance=MemoryImportance.HIGH,
        )
    )

    assert result.total_matches == 1
    assert result.memories[0].importance == MemoryImportance.CRITICAL


def test_search_limit() -> None:
    """Search should respect the requested limit."""

    repository = create_repository()

    for i in range(5):
        repository.add(
            create_memory(
                str(i),
                f"Memory {i}",
            )
        )

    result = repository.search(
        MemoryQuery(
            limit=2,
        )
    )

    assert result.total_matches == 5
    assert result.returned_count == 2
    assert result.truncated is True
    assert len(result.memories) == 2
