"""Defines the result model returned by the Nexus AI memory system.

This module contains the ``MemoryResult`` dataclass, which represents the
outcome of a memory retrieval operation.

Using a dedicated result object keeps the public memory API extensible by
allowing additional metadata to be returned alongside the retrieved
memories.
"""

from dataclasses import dataclass, field

from ai.memory_record import MemoryRecord


@dataclass(slots=True)
class MemoryResult:
    """Represents the result of a memory search.

    A memory result contains the memories returned by a search operation
    together with useful metadata describing the search.

    Attributes:
        memories: The retrieved memory records.
        total_matches: Total number of matching memories.
        returned_count: Number of memories returned.
        truncated: Indicates whether additional matching memories exist.
    """

    memories: list[MemoryRecord] = field(default_factory=list)
    total_matches: int = 0
    returned_count: int = 0
    truncated: bool = False
