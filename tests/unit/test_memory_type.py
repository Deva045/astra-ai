"""
Unit tests for the MemoryType enumeration.
"""

from __future__ import annotations

from ai.memory_type import MemoryType


class TestMemoryType:
    """
    Tests for the MemoryType enumeration.
    """

    def test_memory_type_values(self) -> None:
        """
        Verify all memory type values.
        """
        assert MemoryType.SHORT_TERM.value == "short_term"
        assert MemoryType.LONG_TERM.value == "long_term"
        assert MemoryType.SYSTEM.value == "system"
        assert MemoryType.USER.value == "user"
        assert MemoryType.FACT.value == "fact"
        assert MemoryType.PREFERENCE.value == "preference"
        assert MemoryType.TASK.value == "task"
        assert MemoryType.CONVERSATION.value == "conversation"

    def test_memory_type_count(self) -> None:
        """
        Verify the number of memory types.
        """
        assert len(MemoryType) == 8

    def test_memory_type_lookup(self) -> None:
        """
        Verify lookup by value.
        """
        assert MemoryType("short_term") is MemoryType.SHORT_TERM
        assert MemoryType("long_term") is MemoryType.LONG_TERM
        assert MemoryType("system") is MemoryType.SYSTEM
        assert MemoryType("user") is MemoryType.USER
        assert MemoryType("fact") is MemoryType.FACT
        assert MemoryType("preference") is MemoryType.PREFERENCE
        assert MemoryType("task") is MemoryType.TASK
        assert MemoryType("conversation") is MemoryType.CONVERSATION

    def test_memory_type_names(self) -> None:
        """
        Verify enumeration names.
        """
        assert MemoryType.SHORT_TERM.name == "SHORT_TERM"
        assert MemoryType.LONG_TERM.name == "LONG_TERM"
        assert MemoryType.SYSTEM.name == "SYSTEM"
        assert MemoryType.USER.name == "USER"
        assert MemoryType.FACT.name == "FACT"
        assert MemoryType.PREFERENCE.name == "PREFERENCE"
        assert MemoryType.TASK.name == "TASK"
        assert MemoryType.CONVERSATION.name == "CONVERSATION"
