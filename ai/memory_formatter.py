"""Formatting utilities for the Nexus AI memory system.

This module defines the ``MemoryFormatter``, which converts memory
records into human-readable text representations.

The formatter is presentation-only and contains no business logic,
making it reusable by the CLI, GUI, logging, and debugging tools.
"""

from __future__ import annotations

from ai.memory_record import MemoryRecord


class MemoryFormatter:
    """Formats memory records."""

    @staticmethod
    def format(memory: MemoryRecord) -> str:
        """Format a memory record.

        Args:
            memory: Memory record.

        Returns:
            Human-readable representation.
        """
        return (
            f"[{memory.memory_type.value}] "
            f"{memory.content} "
            f"(importance={memory.importance.value}, "
            f"accesses={memory.access_count})"
        )

    @staticmethod
    def format_many(
        memories: list[MemoryRecord],
    ) -> str:
        """Format multiple memory records.

        Args:
            memories: Memory records.

        Returns:
            Multi-line formatted string.
        """
        if not memories:
            return "No memories."

        return "\n".join(
            MemoryFormatter.format(memory)
            for memory in memories
        )
