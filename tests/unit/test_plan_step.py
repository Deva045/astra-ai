"""
Unit tests for the PlanStep model.
"""

from __future__ import annotations

from ai.plan_status import PlanStatus
from ai.plan_step import PlanStep


class TestPlanStep:
    """
    Tests for the PlanStep model.
    """

    def test_default_values(self) -> None:
        """
        Verify default values.
        """
        step = PlanStep(
            id=1,
            title="Create folder",
        )

        assert step.id == 1
        assert step.title == "Create folder"
        assert step.description == ""
        assert step.status == PlanStatus.PENDING
        assert step.depends_on == []

    def test_custom_values(self) -> None:
        """
        Verify custom initialization.
        """
        step = PlanStep(
            id=2,
            title="Create file",
            description="Create main.py",
            status=PlanStatus.RUNNING,
            depends_on=[1],
        )

        assert step.id == 2
        assert step.title == "Create file"
        assert step.description == "Create main.py"
        assert step.status == PlanStatus.RUNNING
        assert step.depends_on == [1]
