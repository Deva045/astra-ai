"""Provides the public interface for the Nexus AI memory system.

This module defines the ``MemoryManager``, which coordinates all memory
operations for the application. It serves as the primary entry point for
storing, retrieving, updating, deleting, and searching memories.

The manager depends only on the ``MemoryRepository`` abstraction, ensuring
that the memory system remains independent of any specific storage backend.
"""

from ai.memory_query import MemoryQuery
from ai.memory_record import MemoryRecord
from ai.memory_repository import MemoryRepository
from ai.memory_result import MemoryResult


class MemoryManager:
    """Coordinates memory operations for the application.

    The memory manager provides a storage-agnostic API that delegates all
    persistence operations to a ``MemoryRepository`` implementation.

    Attributes:
        _repository: The repository responsible for storing and retrieving
            memory records.
    """

    def __init__(self, repository: MemoryRepository) -> None:
        """Initialize the memory manager.

        Args:
            repository: Repository implementation used for persistence.
        """
        self._repository = repository

    def add_memory(self, memory: MemoryRecord) -> None:
        """Store a new memory.

        Args:
            memory: The memory record to store.
        """
        self._repository.add(memory)

    def get_memory(self, memory_id: str) -> MemoryRecord | None:
        """Retrieve a memory by its identifier.

        Args:
            memory_id: Unique identifier of the memory.

        Returns:
            The matching memory if found; otherwise ``None``.
        """
        return self._repository.get(memory_id)

    def update_memory(self, memory: MemoryRecord) -> None:
        """Update an existing memory.

        Args:
            memory: Updated memory record.
        """
        self._repository.update(memory)

    def delete_memory(self, memory_id: str) -> None:
        """Delete a memory.

        Args:
            memory_id: Unique identifier of the memory.
        """
        self._repository.delete(memory_id)

    def search_memories(self, query: MemoryQuery) -> MemoryResult:
        """Search for memories.

        Args:
            query: Search criteria.

        Returns:
            Matching memories.
        """
        return self._repository.search(query)

    def list_memories(self) -> list[MemoryRecord]:
        """Return all stored memories.

        Returns:
            A list of all memory records.
        """
        return self._repository.list_all()

    def clear_memories(self) -> None:
        """Remove all stored memories."""
        self._repository.clear()

    def memory_count(self) -> int:
        """Return the number of stored memories.

        Returns:
            Total number of memories.
        """
        return self._repository.count()
