"""Provides statistics for the Nexus AI memory system.

This module defines the ``MemoryStatistics`` class, which computes useful
statistics from a collection of memory records.

The statistics are intended for diagnostics, monitoring, and future GUI
visualization without depending on any storage backend.
"""

from __future__ import annotations

from collections import Counter

from ai.memory_importance import MemoryImportance
from ai.memory_record import MemoryRecord
from ai.memory_type import MemoryType


class MemoryStatistics:
    """Computes statistics for memory records."""

    @staticmethod
    def total(memories: list[MemoryRecord]) -> int:
        """Return the total number of memories.

        Args:
            memories: Memory records.

        Returns:
            Total memory count.
        """
        return len(memories)

    @staticmethod
    def by_type(
        memories: list[MemoryRecord],
    ) -> dict[MemoryType, int]:
        """Count memories by type.

        Args:
            memories: Memory records.

        Returns:
            Mapping of memory type to count.
        """
        counts = Counter(
            memory.memory_type
            for memory in memories
        )

        return {
            memory_type: counts.get(memory_type, 0)
            for memory_type in MemoryType
        }

    @staticmethod
    def by_importance(
        memories: list[MemoryRecord],
    ) -> dict[MemoryImportance, int]:
        """Count memories by importance.

        Args:
            memories: Memory records.

        Returns:
            Mapping of importance level to count.
        """
        counts = Counter(
            memory.importance
            for memory in memories
        )

        return {
            importance: counts.get(importance, 0)
            for importance in MemoryImportance
        }

    @staticmethod
    def total_accesses(
        memories: list[MemoryRecord],
    ) -> int:
        """Return the total access count.

        Args:
            memories: Memory records.

        Returns:
            Sum of all access counts.
        """
        return sum(
            memory.access_count
            for memory in memories
        )

    @staticmethod
    def average_accesses(
        memories: list[MemoryRecord],
    ) -> float:
        """Return the average access count.

        Args:
            memories: Memory records.

        Returns:
            Average access count. Returns 0.0 if no memories exist.
        """
        if not memories:
            return 0.0

        return (
            MemoryStatistics.total_accesses(memories)
            / len(memories)
        )
