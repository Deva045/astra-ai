"""Defines the core memory record model used throughout the Nexus AI memory system.

This module contains the ``MemoryRecord`` dataclass, which represents a single
memory managed by the application.

The model is intentionally storage-agnostic and contains no persistence,
serialization, or business logic. It serves as the central domain object for
the memory system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ai.memory_importance import MemoryImportance
from ai.memory_type import MemoryType


@dataclass(slots=True)
class MemoryRecord:
    """Represents a single memory stored by the memory system.

    A memory record contains the information required to identify,
    classify, prioritize, and retrieve a memory. It is designed to be
    independent of any storage backend, allowing the same model to be
    used with SQLite, ChromaDB, or future implementations.

    Attributes:
        id: Unique identifier for the memory.
        content: The textual content of the memory.
        memory_type: The category of the memory.
        importance: The importance level assigned to the memory.
        created_at: The timestamp when the memory was created.
        updated_at: The timestamp of the most recent modification.
        last_accessed: The timestamp of the last retrieval.
        access_count: The number of times the memory has been accessed.
        metadata: Optional structured metadata associated with the memory.
    """

    id: str
    content: str
    memory_type: MemoryType
    importance: MemoryImportance
    created_at: datetime
    updated_at: datetime
    last_accessed: datetime
    access_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
