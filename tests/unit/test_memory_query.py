"""
Unit tests for the MemoryQuery model.
"""

from __future__ import annotations

from ai.memory_importance import MemoryImportance
from ai.memory_query import MemoryQuery
from ai.memory_type import MemoryType


class TestMemoryQuery:
    """
    Tests for the MemoryQuery model.
    """

    def test_default_query(self) -> None:
        """
        Verify a newly created query uses the default values.
        """
        query = MemoryQuery()

        assert query.text == ""
        assert query.memory_types == []
        assert query.minimum_importance is None
        assert query.limit == 10

    def test_custom_query(self) -> None:
        """
        Verify custom query values are stored.
        """
        query = MemoryQuery(
            text="python",
            memory_types=[
                MemoryType.FACT,
                MemoryType.USER,
            ],
            minimum_importance=MemoryImportance.HIGH,
            limit=5,
        )

        assert query.text == "python"
        assert query.memory_types == [
            MemoryType.FACT,
            MemoryType.USER,
        ]
        assert query.minimum_importance is MemoryImportance.HIGH
        assert query.limit == 5

    def test_empty_memory_types(self) -> None:
        """
        Verify memory types default to an empty list.
        """
        query = MemoryQuery()

        assert query.memory_types == []

    def test_default_limit(self) -> None:
        """
        Verify the default search limit.
        """
        query = MemoryQuery()

        assert query.limit == 10

    def test_no_minimum_importance(self) -> None:
        """
        Verify the default minimum importance.
        """
        query = MemoryQuery()

        assert query.minimum_importance is None
