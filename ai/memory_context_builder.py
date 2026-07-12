"""Builds prompt context from retrieved memories.

This module defines the ``MemoryContextBuilder``, which converts memory
search results into a formatted text block suitable for inclusion in AI
prompts.

Separating this responsibility from the AI engine keeps the engine
focused on orchestration while making memory presentation reusable and
independently testable.
"""

from __future__ import annotations

from ai.memory_result import MemoryResult


class MemoryContextBuilder:
    """Builds formatted prompt context from memory search results."""

    @staticmethod
    def build(result: MemoryResult) -> str:
        """Build formatted memory context.

        Args:
            result: Memory search result.

        Returns:
            A formatted string containing relevant memories. Returns an
            empty string when no memories are available.
        """
        if not result.memories:
            return ""

        lines = [
            "Relevant memories:",
        ]

        for memory in result.memories:
            lines.append(f"- {memory.content}")

        return "\n".join(lines)
