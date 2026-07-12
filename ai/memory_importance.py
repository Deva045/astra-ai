"""Defines memory importance levels used throughout the Nexus AI memory system.

This module contains the ``MemoryImportance`` enumeration, which represents
the relative importance of stored memories.

Using an enumeration instead of raw numeric values improves readability,
type safety, and consistency across the project while allowing future
ranking and pruning strategies.
"""

from enum import Enum


class MemoryImportance(str, Enum):
    """Represents the importance level assigned to a memory.

    Importance levels help the memory system prioritize which memories
    should be retained, retrieved, summarized, or discarded.

    Attributes:
        LOW: Low-priority memory.
        MEDIUM: Standard importance.
        HIGH: Important memory that should generally be retained.
        CRITICAL: Extremely important memory that should always be preserved.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
