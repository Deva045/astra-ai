"""
Task status definitions for Astra AI.

This module defines the lifecycle states used by the task management
subsystem introduced in Sprint 7.
"""

from __future__ import annotations

from enum import Enum


class TaskStatus(str, Enum):
    """Represents the lifecycle state of a task."""

    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

    @property
    def is_finished(self) -> bool:
        """Return True if the task is in a terminal state."""
        return self in (
            TaskStatus.COMPLETED,
            TaskStatus.FAILED,
            TaskStatus.CANCELLED,
        )

    @property
    def is_active(self) -> bool:
        """Return True if the task is still managed by the scheduler."""
        return self in (
            TaskStatus.PENDING,
            TaskStatus.RUNNING,
            TaskStatus.PAUSED,
        )

    @property
    def can_execute(self) -> bool:
        """Return True if execution may start or continue."""
        return self in (
            TaskStatus.PENDING,
            TaskStatus.RUNNING,
        )
