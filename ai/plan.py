"""
Execution plan model for Astra AI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from ai.plan_status import PlanStatus
from ai.plan_step import PlanStep


@dataclass(slots=True)
class Plan:
    """
    Represents a complete execution plan.
    """

    goal: str
    steps: list[PlanStep] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def add_step(self, step: PlanStep) -> None:
        """
        Add a step to the execution plan.
        """
        self.steps.append(step)

    def step_count(self) -> int:
        """
        Return the total number of steps.
        """
        return len(self.steps)

    def completed_steps(self) -> list[PlanStep]:
        """
        Return all completed steps.
        """
        return [
            step
            for step in self.steps
            if step.status == PlanStatus.COMPLETED
        ]

    def pending_steps(self) -> list[PlanStep]:
        """
        Return all pending steps.
        """
        return [
            step
            for step in self.steps
            if step.status == PlanStatus.PENDING
        ]

    def is_complete(self) -> bool:
        """
        Return True if every step has completed.
        """
        return (
            len(self.steps) > 0
            and all(
                step.status == PlanStatus.COMPLETED
                for step in self.steps
            )
        )
