"""
Unit tests for the PlanStatus enum.
"""

from __future__ import annotations

from ai.plan_status import PlanStatus


class TestPlanStatus:
    """
    Tests for the PlanStatus enum.
    """

    def test_enum_values(self) -> None:
        """
        Verify all enum values.
        """
        assert PlanStatus.PENDING.value == "pending"
        assert PlanStatus.RUNNING.value == "running"
        assert PlanStatus.COMPLETED.value == "completed"
        assert PlanStatus.FAILED.value == "failed"
        assert PlanStatus.SKIPPED.value == "skipped"

    def test_enum_member_count(self) -> None:
        """
        Verify the number of enum members.
        """
        assert len(PlanStatus) == 5
