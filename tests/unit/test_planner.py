"""
Unit tests for the Planner.
"""

from __future__ import annotations

from ai.plan_status import PlanStatus
from ai.planner import Planner


class TestPlanner:
    """
    Tests for the Planner.
    """

    def setup_method(self) -> None:
        """
        Create a fresh planner before each test.
        """
        self.planner = Planner()

    def test_empty_goal(self) -> None:
        """
        An empty goal should produce an empty plan.
        """
        plan = self.planner.create_plan("")

        assert plan.goal == ""
        assert plan.step_count() == 0
        assert not plan.is_complete()

    def test_goal_is_trimmed(self) -> None:
        """
        Leading and trailing whitespace should be removed.
        """
        plan = self.planner.create_plan("   Open calculator   ")

        assert plan.goal == "Open calculator"

    def test_single_step_plan(self) -> None:
        """
        A simple goal should create one plan step.
        """
        plan = self.planner.create_plan("Open calculator")

        assert plan.step_count() == 1

    def test_step_id(self) -> None:
        """
        The first step should have ID 1.
        """
        plan = self.planner.create_plan("Open calculator")

        assert plan.steps[0].id == 1

    def test_step_title(self) -> None:
        """
        The step title should match the goal.
        """
        plan = self.planner.create_plan("Open calculator")

        assert plan.steps[0].title == "Open calculator"

    def test_step_description(self) -> None:
        """
        The default description should be assigned.
        """
        plan = self.planner.create_plan("Open calculator")

        assert (
            plan.steps[0].description
            == "Execute the requested task."
        )

    def test_step_default_status(self) -> None:
        """
        New steps should start in the pending state.
        """
        plan = self.planner.create_plan("Open calculator")

        assert (
            plan.steps[0].status
            == PlanStatus.PENDING
        )

    def test_pending_steps(self) -> None:
        """
        The created step should appear in pending steps.
        """
        plan = self.planner.create_plan("Open calculator")

        assert len(plan.pending_steps()) == 1

    def test_completed_steps_initially_empty(self) -> None:
        """
        A new plan should not contain completed steps.
        """
        plan = self.planner.create_plan("Open calculator")

        assert plan.completed_steps() == []

    def test_plan_is_not_complete(self) -> None:
        """
        A new plan should not be complete.
        """
        plan = self.planner.create_plan("Open calculator")

        assert not plan.is_complete()
