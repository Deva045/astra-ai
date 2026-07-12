"""Extracts long-term memories from conversation.

This module provides the ``MemoryExtractor`` class, which analyzes user
messages and determines whether they should be stored as long-term
memories.

The initial implementation uses simple rule-based heuristics. The design
is intentionally extensible so that future versions can incorporate
machine learning or LLM-based extraction without affecting the rest of
the application.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from ai.memory_importance import MemoryImportance
from ai.memory_record import MemoryRecord
from ai.memory_type import MemoryType


class MemoryExtractor:
    """Extracts structured memories from user messages."""

    _PREFERENCE_PREFIXES: tuple[str, ...] = (
        "i like",
        "i love",
        "i prefer",
        "my favorite",
        "my favourite",
    )

    _USER_PREFIXES: tuple[str, ...] = (
        "my name is",
        "i am",
        "i'm",
    )

    _FACT_PREFIXES: tuple[str, ...] = (
        "remember that",
        "remember",
    )

    def extract(self, text: str) -> MemoryRecord | None:
        """Extract a memory from user text.

        Args:
            text: User message.

        Returns:
            A populated ``MemoryRecord`` if the message represents a
            useful long-term memory; otherwise ``None``.
        """
        normalized = text.strip()

        if not normalized:
            return None

        lowered = normalized.lower()

        memory_type = self._detect_type(lowered)

        if memory_type is None:
            return None

        importance = self._detect_importance(memory_type)

        now = datetime.now()

        return MemoryRecord(
            id=str(uuid4()),
            content=normalized,
            memory_type=memory_type,
            importance=importance,
            created_at=now,
            updated_at=now,
            last_accessed=now,
            access_count=0,
            metadata={},
        )

    def _detect_type(self, text: str) -> MemoryType | None:
        """Determine the memory type.

        Args:
            text: Normalized user text.

        Returns:
            The detected memory type, or ``None`` if the message should
            not be stored.
        """
        if text.startswith(self._USER_PREFIXES):
            return MemoryType.USER

        if text.startswith(self._PREFERENCE_PREFIXES):
            return MemoryType.PREFERENCE

        if text.startswith(self._FACT_PREFIXES):
            return MemoryType.FACT

        return None

    def _detect_importance(
        self,
        memory_type: MemoryType,
    ) -> MemoryImportance:
        """Determine the importance of a memory.

        Args:
            memory_type: Detected memory type.

        Returns:
            The assigned importance level.
        """
        if memory_type is MemoryType.USER:
            return MemoryImportance.CRITICAL

        if memory_type is MemoryType.PREFERENCE:
            return MemoryImportance.HIGH

        if memory_type is MemoryType.FACT:
            return MemoryImportance.MEDIUM

        return MemoryImportance.LOW
