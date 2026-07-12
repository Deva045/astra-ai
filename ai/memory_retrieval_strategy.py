"""Defines memory retrieval strategies for the Nexus AI memory system.

This module contains the ``MemoryRetrievalStrategy`` enumeration, which
specifies the strategy used when retrieving memories.

Using an enumeration keeps retrieval behavior configurable while
remaining independent of any specific storage backend.
"""

from __future__ import annotations

from enum import Enum


class MemoryRetrievalStrategy(str, Enum):
    """Represents a memory retrieval strategy.

    Attributes:
        RECENT:
            Return the most recently created memories.

        MOST_ACCESSED:
            Return the most frequently accessed memories.

        IMPORTANCE:
            Prioritize memories with the highest importance.

        RELEVANCE:
            Return memories most relevant to the search query.

        HYBRID:
            Combine multiple ranking signals.
    """

    RECENT = "recent"
    MOST_ACCESSED = "most_accessed"
    IMPORTANCE = "importance"
    RELEVANCE = "relevance"
    HYBRID = "hybrid"
