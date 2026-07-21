"""
Workflow step model for Astra AI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class WorkflowStep:
    """Represents a single step in a workflow."""

    step_id: str
    name: str
    description: str = ""
    completed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def complete(self) -> None:
        """Mark the step as completed."""
        self.completed = True

    def reset(self) -> None:
        """Reset the step state."""
        self.completed = False
