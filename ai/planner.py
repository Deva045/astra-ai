
"""
Planner for Astra AI.

Responsible for converting high-level user goals into
structured execution plans.
"""

from __future__ import annotations

from ai.plan import Plan
from ai.plan_parser import PlanParser
from ai.execution_result import ExecutionResult
from ai.plan_executor import PlanExecutor
from ai.plan_step import PlanStep


class Planner:
    """
    Builds execution plans from user requests.
    """

    def __init__(self) -> None:
        self._parser = PlanParser()

    def create_plan(self, goal: str) -> Plan:
        """
        Create an execution plan for the supplied goal.
        """

        goal = goal.strip()

        plan = Plan(goal=goal)

        if not goal:
            return plan

        lowered = goal.lower()

        if (
            "python project" in lowered
            or "project called" in lowered
        ):
            self._plan_python_project(
                plan,
                goal,
            )
            return plan

        instructions = self._parser.parse(goal)

        if len(instructions) > 1:
            self._plan_multiple(
                plan,
                instructions,
            )
            return plan

        instruction = instructions[0] if instructions else goal
        lowered = instruction.lower()

        if lowered.startswith("create folder"):
            self._plan_folder_creation(
                plan,
                instruction,
            )
            return plan

        if lowered.startswith("create file"):
            self._plan_file_creation(
                plan,
                instruction,
            )
            return plan

        self._plan_generic(
            plan,
            instruction,
        )

        return plan


    def plan_and_execute(
        self,
        goal: str,
        executor: PlanExecutor,
    ) -> ExecutionResult:
        """
        Create a plan and execute it.
        """

        plan = self.create_plan(
            goal
        )

        return executor.execute_with_result(
            plan
        )


    def _plan_python_project(
        self,
        plan: Plan,
        goal: str,
    ) -> None:
        """
        Create a standard Python project plan.
        """

        project_name = self._extract_project_name(
            goal
        )

        self._add_step(
            plan,
            f'Create project folder "{project_name}"',
        )

        self._add_step(
            plan,
            "Create main.py",
        )

        self._add_step(
            plan,
            "Create requirements.txt",
        )

        self._add_step(
            plan,
            "Verify project structure",
        )

    def _plan_folder_creation(
        self,
        plan: Plan,
        goal: str,
    ) -> None:
        """
        Create a folder creation plan.
        """

        folder = goal[len("Create folder"):].strip()

        self._add_step(
            plan,
            f"Create folder {folder}",
        )

    def _plan_file_creation(
        self,
        plan: Plan,
        goal: str,
    ) -> None:
        """
        Create a file creation plan.
        """

        filename = goal[len("Create file"):].strip()

        self._add_step(
            plan,
            f"Create file {filename}",
        )

    def _plan_multiple(
        self,
        plan: Plan,
        instructions: list[str],
    ) -> None:
        """
        Build a plan from multiple instructions.
        """

        for instruction in instructions:

            lowered = instruction.lower()

            if lowered.startswith("create folder"):
                self._plan_folder_creation(
                    plan,
                    instruction,
                )

            elif lowered.startswith("create file"):
                self._plan_file_creation(
                    plan,
                    instruction,
                )

            else:
                self._plan_generic(
                    plan,
                    instruction,
                )

    def _plan_generic(
        self,
        plan: Plan,
        goal: str,
    ) -> None:
        """
        Generic planning fallback.
        """

        self._add_step(
            plan,
            goal,
            "Execute the requested task.",
        )

    def _add_step(
        self,
        plan: Plan,
        title: str,
        description: str = "",
    ) -> None:
        """
        Add a step to the plan.
        """

        plan.add_step(
            PlanStep(
                id=plan.step_count() + 1,
                title=title,
                description=description,
            )
        )

    def _extract_project_name(
        self,
        goal: str,
    ) -> str:
        """
        Extract the project name.
        """

        lowered = goal.lower()

        if "called" in lowered:
            return goal.split(
                "called",
                1,
            )[1].strip()

        words = goal.split()

        if words:
            return words[-1]

        return "Project"
