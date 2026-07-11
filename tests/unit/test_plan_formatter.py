"""
Unit tests for the PlanFormatter.
"""

from __future__ import annotations

from ai.plan import Plan
from ai.plan_formatter import PlanFormatter
from ai.plan_step import PlanStep


class TestPlanFormatter:
    """
    Tests for the PlanFormatter.
    """

    def test_empty_plan(self) -> None:
        """
        Empty plans should display a placeholder.
        """
        plan = Plan(goal="Demo")

        text = PlanFormatter.format(plan)

        assert "Goal: Demo" in text
        assert "No steps available." in text

    def test_single_step(self) -> None:
        """
        Single-step plans should be formatted correctly.
        """
        plan = Plan(goal="Demo")

        plan.add_step(
            PlanStep(
                id=1,
                title="Create folder Demo",
            )
        )

        text = PlanFormatter.format(plan)

        assert "Goal: Demo" in text
        assert "1. Create folder Demo" in text

    def test_multiple_steps(self) -> None:
        """
        Multiple-step plans should preserve order.
        """
        plan = Plan(goal="Demo")

        plan.add_step(
            PlanStep(
                id=1,
                title="Create folder Demo",
            )
        )

        plan.add_step(
            PlanStep(
                id=2,
                title="Create main.py",
            )
        )

        text = PlanFormatter.format(plan)

        assert "1. Create folder Demo" in text
        assert "2. Create main.py" in text

    def test_description(self) -> None:
        """
        Step descriptions should be displayed.
        """
        plan = Plan(goal="Demo")

        plan.add_step(
            PlanStep(
                id=1,
                title="Create folder Demo",
                description="Creates the project directory.",
            )
        )

        text = PlanFormatter.format(plan)

        assert "Creates the project directory." in text
