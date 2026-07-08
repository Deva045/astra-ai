"""
Execution status for plan steps.
"""

from __future__ import annotations

from enum import Enum


class PlanStatus(str, Enum):
    """
    Represents the execution state of a plan step.
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
