"""Validation utilities for the Nexus AI memory system.

This module defines the ``MemoryValidator``, which validates memory
records before they are stored or updated.

Validation is intentionally separated from the repository and manager to
keep business rules centralized and reusable.
"""

from __future__ import annotations

from ai.memory_record import MemoryRecord


class MemoryValidator:
    """Validates memory records."""

    @staticmethod
    def validate(memory: MemoryRecord) -> None:
        """Validate a memory record.

        Args:
            memory: Memory record to validate.

        Raises:
            ValueError: If the memory record is invalid.
        """
        if not memory.id.strip():
            raise ValueError("Memory id cannot be empty.")

        if not memory.content.strip():
            raise ValueError("Memory content cannot be empty.")

        if memory.access_count < 0:
            raise ValueError(
                "Memory access count cannot be negative."
            )

        if memory.created_at > memory.updated_at:
            raise ValueError(
                "created_at cannot be after updated_at."
            )

        if memory.updated_at > memory.last_accessed:
            raise ValueError(
                "updated_at cannot be after last_accessed."
            )

        if memory.metadata is None:
            raise ValueError(
                "Memory metadata cannot be None."
            )
