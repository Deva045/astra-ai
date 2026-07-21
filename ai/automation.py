"""
Automation model for Astra AI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class Automation:
    """Represents an automation task."""

    automation_id: str
    name: str
    description: str = ""
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def enable(self) -> None:
        """Enable the automation."""
        self.enabled = True

    def disable(self) -> None:
        """Disable the automation."""
        self.enabled = False

    def update_metadata(self, key: str, value: Any) -> None:
        """Store automation metadata."""
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Retrieve automation metadata."""
        return self.metadata.get(key, default)
