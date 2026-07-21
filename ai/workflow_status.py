"""
Workflow status definitions for Astra AI.
"""

from __future__ import annotations

from enum import Enum


class WorkflowStatus(str, Enum):
    """Represents the lifecycle of a workflow."""

    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

    @property
    def is_finished(self) -> bool:
        """Return True if the workflow has reached a terminal state."""
        return self in {
            WorkflowStatus.COMPLETED,
            WorkflowStatus.FAILED,
            WorkflowStatus.CANCELLED,
        }

    @property
    def is_active(self) -> bool:
        """Return True if the workflow is currently active."""
        return self in {
            WorkflowStatus.PENDING,
            WorkflowStatus.RUNNING,
            WorkflowStatus.PAUSED,
        }

    @property
    def can_execute(self) -> bool:
        """Return True if the workflow can continue execution."""
        return self in {
            WorkflowStatus.PENDING,
            WorkflowStatus.RUNNING,
        }
