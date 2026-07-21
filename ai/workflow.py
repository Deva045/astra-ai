"""
Workflow model for Astra AI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from ai.workflow_status import WorkflowStatus
from ai.workflow_step import WorkflowStep


@dataclass(slots=True)
class Workflow:
    """Represents a workflow composed of multiple steps."""

    workflow_id: str
    name: str
    description: str = ""
    status: WorkflowStatus = WorkflowStatus.PENDING
    steps: list[WorkflowStep] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    started_at: datetime | None = None
    completed_at: datetime | None = None

    def start(self) -> None:
        """Start the workflow."""
        self.status = WorkflowStatus.RUNNING
        self.started_at = datetime.now(UTC)

    def complete(self) -> None:
        """Mark the workflow as completed."""
        self.status = WorkflowStatus.COMPLETED
        self.completed_at = datetime.now(UTC)

    def fail(self) -> None:
        """Mark the workflow as failed."""
        self.status = WorkflowStatus.FAILED
        self.completed_at = datetime.now(UTC)

    def cancel(self) -> None:
        """Cancel the workflow."""
        self.status = WorkflowStatus.CANCELLED
        self.completed_at = datetime.now(UTC)

    def add_step(self, step: WorkflowStep) -> None:
        """Add a step to the workflow."""
        self.steps.append(step)

    @property
    def total_steps(self) -> int:
        """Return the total number of steps."""
        return len(self.steps)

    @property
    def completed_steps(self) -> int:
        """Return the number of completed steps."""
        return sum(step.completed for step in self.steps)

    @property
    def progress(self) -> float:
        """Return workflow completion percentage."""
        if not self.steps:
            return 0.0
        return (self.completed_steps / self.total_steps) * 100.0
