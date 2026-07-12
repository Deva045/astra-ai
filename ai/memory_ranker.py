"""Ranks memories returned by the memory system.

This module defines the ``MemoryRanker``, which orders retrieved memories
according to configurable ranking rules.

The initial implementation ranks memories by:

1. Importance
2. Access count
3. Last accessed time

Future implementations may incorporate semantic similarity scores or
embedding distances while preserving the same public interface.
"""

from __future__ import annotations

from ai.memory_importance import MemoryImportance
from ai.memory_record import MemoryRecord


class MemoryRanker:
    """Ranks memory records."""

    _IMPORTANCE_SCORE: dict[MemoryImportance, int] = {
        MemoryImportance.LOW: 0,
        MemoryImportance.MEDIUM: 1,
        MemoryImportance.HIGH: 2,
        MemoryImportance.CRITICAL: 3,
    }

    @classmethod
    def rank(
        cls,
        memories: list[MemoryRecord],
    ) -> list[MemoryRecord]:
        """Return memories ranked by priority.

        Args:
            memories: Memory records to rank.

        Returns:
            Ranked memory records.
        """
        return sorted(
            memories,
            key=lambda memory: (
                cls._IMPORTANCE_SCORE[memory.importance],
                memory.access_count,
                memory.last_accessed,
            ),
            reverse=True,
        )
