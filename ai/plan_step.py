"""
Plan step model for Astra AI.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ai.plan_status import PlanStatus


@dataclass(slots=True)
class PlanStep:
    """
    Represents a single step in an execution plan.
    """

    id: int
    title: str
    description: str = ""
    status: PlanStatus = PlanStatus.PENDING
    depends_on: list[int] = field(default_factory=list)
