"""
Execution monitor for Astra AI.

Tracks the execution state, progress, timing, and errors for a running task.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class ExecutionMonitor:
    """Monitors the execution of a task."""

    task_name: str = ""
    total_steps: int = 0
    completed_steps: int = 0
    current_step: str = ""
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error: str | None = None
    running: bool = False
    successful: bool = False

    def start(self, task_name: str, total_steps: int) -> None:
        """Start monitoring a task."""
        self.task_name = task_name
        self.total_steps = max(0, total_steps)
        self.completed_steps = 0
        self.current_step = ""
        self.started_at = datetime.now(UTC)
        self.finished_at = None
        self.error = None
        self.running = True
        self.successful = False

    def update_step(self, completed_steps: int, step_name: str) -> None:
        """Update the current execution step."""
        self.completed_steps = min(max(0, completed_steps), self.total_steps)
        self.current_step = step_name

    def complete(self) -> None:
        """Mark execution as completed successfully."""
        self.completed_steps = self.total_steps
        self.finished_at = datetime.now(UTC)
        self.running = False
        self.successful = True

    def fail(self, message: str) -> None:
        """Mark execution as failed."""
        self.error = message
        self.finished_at = datetime.now(UTC)
        self.running = False
        self.successful = False

    def reset(self) -> None:
        """Reset the monitor."""
        self.task_name = ""
        self.total_steps = 0
        self.completed_steps = 0
        self.current_step = ""
        self.started_at = None
        self.finished_at = None
        self.error = None
        self.running = False
        self.successful = False

    @property
    def progress(self) -> float:
        """Return completion percentage."""
        if self.total_steps == 0:
            return 0.0
        return (self.completed_steps / self.total_steps) * 100.0

    @property
    def duration(self) -> float | None:
        """Return execution duration in seconds."""
        if self.started_at is None:
            return None

        end = self.finished_at or datetime.now(UTC)
        return (end - self.started_at).total_seconds()
