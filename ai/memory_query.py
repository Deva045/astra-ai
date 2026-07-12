"""Defines the query model used to search the Nexus AI memory system.

This module contains the ``MemoryQuery`` dataclass, which encapsulates the
criteria used when searching for memories.

Using a dedicated query object keeps the memory API clean, extensible, and
strongly typed as additional search options are introduced over time.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ai.memory_importance import MemoryImportance
from ai.memory_type import MemoryType


@dataclass(slots=True)
class MemoryQuery:
    """Represents a request to search the memory system.

    A memory query contains optional filters that the memory repository
    or memory manager can use to locate relevant memories.

    Attributes:
        text: Free-text search query.
        memory_types: Memory categories to include.
        minimum_importance: Lowest acceptable importance level.
        limit: Maximum number of memories to return.
        include_system: Whether system memories should be included.
        include_conversation: Whether conversation memories should be
            included.
        sort_by: Optional sort strategy reserved for future use.
    """

    text: str = ""
    memory_types: list[MemoryType] = field(default_factory=list)
    minimum_importance: MemoryImportance | None = None
    limit: int = 10

    # Future-ready search options
    include_system: bool = True
    include_conversation: bool = True
    sort_by: str | None = None
