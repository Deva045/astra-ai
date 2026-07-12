"""Defines the abstract repository interface for the Nexus AI memory system.

This module declares the ``MemoryRepository`` abstract base class, which
defines the operations that every memory storage backend must implement.

Concrete implementations (such as SQLite or ChromaDB) should inherit from
this interface. The rest of the application communicates only through this
abstraction, keeping the memory system storage-agnostic.
"""

from abc import ABC, abstractmethod

from ai.memory_query import MemoryQuery
from ai.memory_record import MemoryRecord
from ai.memory_result import MemoryResult


class MemoryRepository(ABC):
    """Abstract interface for memory storage backends."""

    @abstractmethod
    def add(self, memory: MemoryRecord) -> None:
        """Store a memory record.

        Args:
            memory: The memory record to store.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, memory_id: str) -> MemoryRecord | None:
        """Retrieve a memory by its unique identifier.

        Args:
            memory_id: Unique memory identifier.

        Returns:
            The matching memory if found; otherwise ``None``.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, memory: MemoryRecord) -> None:
        """Update an existing memory record.

        Args:
            memory: The updated memory record.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, memory_id: str) -> None:
        """Delete a memory from storage.

        Args:
            memory_id: Unique memory identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def search(self, query: MemoryQuery) -> MemoryResult:
        """Search for memories matching the supplied query.

        Args:
            query: Search criteria.

        Returns:
            A structured memory search result.
        """
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[MemoryRecord]:
        """Return all stored memories.

        Returns:
            A list containing every stored memory.
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """Remove all memories from storage."""
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        """Return the number of stored memories.

        Returns:
            Total number of stored memories.
        """
        raise NotImplementedError
