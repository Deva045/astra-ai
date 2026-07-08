"""
Unit tests for the Plan model.
"""

from __future__ import annotations

from ai.plan import Plan
from ai.plan_status import PlanStatus
from ai.plan_step import PlanStep


class TestPlan:
    """
    Tests for the Plan model.
    """

    def test_empty_plan(self) -> None:
        """
        Verify a newly created plan.
        """
        plan = Plan(goal="Build project")

        assert plan.goal == "Build project"
        assert plan.step_count() == 0
        assert plan.completed_steps() == []
        assert plan.pending_steps() == []
        assert not plan.is_complete()

    def test_add_step(self) -> None:
        """
        Verify adding a step.
        """
        plan = Plan(goal="Demo")

        step = PlanStep(
            id=1,
            title="Create folder",
        )

        plan.add_step(step)

        assert plan.step_count() == 1
        assert plan.steps[0] == step

    def test_pending_steps(self) -> None:
        """
        Verify pending step detection.
        """
        plan = Plan(goal="Demo")

        plan.add_step(
            PlanStep(
                id=1,
                title="A",
            )
        )

        plan.add_step(
            PlanStep(
                id=2,
                title="B",
                status=PlanStatus.COMPLETED,
            )
        )

        pending = plan.pending_steps()

        assert len(pending) == 1
        assert pending[0].id == 1

    def test_completed_steps(self) -> None:
        """
        Verify completed step detection.
        """
        plan = Plan(goal="Demo")

        plan.add_step(
            PlanStep(
                id=1,
                title="A",
                status=PlanStatus.COMPLETED,
            )
        )

        completed = plan.completed_steps()

        assert len(completed) == 1
        assert completed[0].id == 1

    def test_is_complete(self) -> None:
        """
        Verify completion detection.
        """
        plan = Plan(goal="Demo")

        plan.add_step(
            PlanStep(
                id=1,
                title="A",
                status=PlanStatus.COMPLETED,
            )
        )

        plan.add_step(
            PlanStep(
                id=2,
                title="B",
                status=PlanStatus.COMPLETED,
            )
        )

        assert plan.is_complete()

    def test_is_not_complete(self) -> None:
        """
        Verify incomplete plans.
        """
        plan = Plan(goal="Demo")

        plan.add_step(
            PlanStep(
                id=1,
                title="A",
                status=PlanStatus.COMPLETED,
            )
        )

        plan.add_step(
            PlanStep(
                id=2,
                title="B",
            )
        )

        assert not plan.is_complete()
