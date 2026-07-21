"""
Event model for Astra AI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class Event:
    """Represents an event emitted within the system."""

    event_id: str
    event_type: str
    source: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    def add_data(self, key: str, value: Any) -> None:
        """Add or update payload data."""
        self.payload[key] = value

    def get_data(self, key: str, default: Any = None) -> Any:
        """Retrieve payload data."""
        return self.payload.get(key, default)
