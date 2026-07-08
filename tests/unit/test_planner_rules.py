"""
Unit tests for rule-based planning.
"""

from __future__ import annotations

from ai.planner import Planner


class TestPlannerRules:
    """
    Tests for the rule-based planner.
    """

    def setup_method(self) -> None:
        self.planner = Planner()

    def test_python_project_plan(self) -> None:
        """
        A Python project request should generate four steps.
        """
        plan = self.planner.create_plan(
            "Create a Python project called Demo"
        )

        assert plan.goal == "Create a Python project called Demo"
        assert plan.step_count() == 4

    def test_project_folder_step(self) -> None:
        """
        The first step should create the project folder.
        """
        plan = self.planner.create_plan(
            "Create a Python project called Demo"
        )

        assert (
            plan.steps[0].title
            == 'Create project folder "Demo"'
        )

    def test_main_file_step(self) -> None:
        """
        The second step should create main.py.
        """
        plan = self.planner.create_plan(
            "Create a Python project called Demo"
        )

        assert plan.steps[1].title == "Create main.py"

    def test_requirements_step(self) -> None:
        """
        The third step should create requirements.txt.
        """
        plan = self.planner.create_plan(
            "Create a Python project called Demo"
        )

        assert (
            plan.steps[2].title
            == "Create requirements.txt"
        )

    def test_verify_step(self) -> None:
        """
        The final step should verify the project.
        """
        plan = self.planner.create_plan(
            "Create a Python project called Demo"
        )

        assert (
            plan.steps[3].title
            == "Verify project structure"
        )

    def test_step_ids_are_sequential(self) -> None:
        """
        Step IDs should start at one and increment.
        """
        plan = self.planner.create_plan(
            "Create a Python project called Demo"
        )

        ids = [step.id for step in plan.steps]

        assert ids == [1, 2, 3, 4]

    def test_generic_request_fallback(self) -> None:
        """
        Unknown requests should fall back to a single step.
        """
        plan = self.planner.create_plan(
            "Open Calculator"
        )

        assert plan.step_count() == 1
        assert plan.steps[0].title == "Open Calculator"

    def test_project_name_extraction(self) -> None:
        """
        The project name should be extracted correctly.
        """
        plan = self.planner.create_plan(
            "Create a Python project called Astra"
        )

        assert (
            plan.steps[0].title
            == 'Create project folder "Astra"'
        )
