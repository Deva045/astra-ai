"""
Task model for Astra AI.

Represents a single managed task within the task management system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from ai.task_status import TaskStatus


@dataclass(slots=True)
class Task:
    """
    Represents a managed task.
    """

    task_id: str
    name: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    progress: int = 0

    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    started_at: datetime | None = None
    completed_at: datetime | None = None

    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def start(self) -> None:
        """Start the task."""
        if self.status == TaskStatus.PENDING:
            self.status = TaskStatus.RUNNING
            self.started_at = datetime.now(UTC)

    def pause(self) -> None:
        """Pause the task."""
        if self.status == TaskStatus.RUNNING:
            self.status = TaskStatus.PAUSED

    def resume(self) -> None:
        """Resume the task."""
        if self.status == TaskStatus.PAUSED:
            self.status = TaskStatus.RUNNING

    def update_progress(self, progress: int) -> None:
        """
        Update task progress.

        Progress is clamped between 0 and 100.
        """
        self.progress = max(0, min(100, progress))

    def complete(self) -> None:
        """Mark the task as completed."""
        self.progress = 100
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now(UTC)

    def fail(self, reason: str = "") -> None:
        """Mark the task as failed."""
        self.status = TaskStatus.FAILED
        self.error = reason
        self.completed_at = datetime.now(UTC)

    def cancel(self) -> None:
        """Cancel the task."""
        self.status = TaskStatus.CANCELLED
        self.completed_at = datetime.now(UTC)

    @property
    def is_finished(self) -> bool:
        """Return True if the task has reached a terminal state."""
        return self.status.is_finished
