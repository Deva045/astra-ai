"""
Unit tests for multi-step planning.
"""

from __future__ import annotations

from ai.planner import Planner


class TestPlannerMultiStep:
    """
    Tests for multi-step planning.
    """

    def setup_method(self) -> None:
        self.planner = Planner()

    def test_folder_creation(self) -> None:
        plan = self.planner.create_plan(
            "Create folder Demo"
        )

        assert plan.step_count() == 1
        assert plan.steps[0].title == "Create folder Demo"

    def test_file_creation(self) -> None:
        plan = self.planner.create_plan(
            "Create file app.py"
        )

        assert plan.step_count() == 1
        assert plan.steps[0].title == "Create file app.py"

    def test_multiple_steps(self) -> None:
        plan = self.planner.create_plan(
            "Create folder Demo. "
            "Create file app.py. "
            "Create file README.md."
        )

        assert plan.step_count() == 3

    def test_step_order(self) -> None:
        plan = self.planner.create_plan(
            "Create folder Demo. "
            "Create file app.py."
        )

        assert plan.steps[0].title == "Create folder Demo"
        assert plan.steps[1].title == "Create file app.py"

    def test_sequential_ids(self) -> None:
        plan = self.planner.create_plan(
            "Create folder Demo. "
            "Create file app.py."
        )

        ids = [step.id for step in plan.steps]

        assert ids == [1, 2]

    def test_generic_instruction_in_multi_plan(self) -> None:
        plan = self.planner.create_plan(
            "Open calculator. "
            "Create folder Demo."
        )

        assert plan.step_count() == 2
        assert plan.steps[0].title == "Open calculator"
        assert plan.steps[1].title == "Create folder Demo"
