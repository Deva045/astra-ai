"""
Unit tests for the MemoryImportance enumeration.
"""

from __future__ import annotations

from ai.memory_importance import MemoryImportance


class TestMemoryImportance:
    """
    Tests for the MemoryImportance enumeration.
    """

    def test_memory_importance_values(self) -> None:
        """
        Verify all importance values.
        """
        assert MemoryImportance.LOW.value == "low"
        assert MemoryImportance.MEDIUM.value == "medium"
        assert MemoryImportance.HIGH.value == "high"
        assert MemoryImportance.CRITICAL.value == "critical"

    def test_memory_importance_count(self) -> None:
        """
        Verify the number of importance levels.
        """
        assert len(MemoryImportance) == 4

    def test_memory_importance_lookup(self) -> None:
        """
        Verify lookup by value.
        """
        assert MemoryImportance("low") is MemoryImportance.LOW
        assert MemoryImportance("medium") is MemoryImportance.MEDIUM
        assert MemoryImportance("high") is MemoryImportance.HIGH
        assert MemoryImportance("critical") is MemoryImportance.CRITICAL

    def test_memory_importance_names(self) -> None:
        """
        Verify enumeration names.
        """
        assert MemoryImportance.LOW.name == "LOW"
        assert MemoryImportance.MEDIUM.name == "MEDIUM"
        assert MemoryImportance.HIGH.name == "HIGH"
        assert MemoryImportance.CRITICAL.name == "CRITICAL"
