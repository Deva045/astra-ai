"""
Schedule model for Astra AI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta


@dataclass(slots=True)
class Schedule:
    """Represents a scheduled task."""

    schedule_id: str
    name: str
    interval: timedelta
    enabled: bool = True
    last_run: datetime | None = None
    next_run: datetime = field(default_factory=lambda: datetime.now(UTC))

    def mark_executed(self) -> None:
        """Update execution timestamps."""
        self.last_run = datetime.now(UTC)
        self.next_run = self.last_run + self.interval

    def enable(self) -> None:
        """Enable the schedule."""
        self.enabled = True

    def disable(self) -> None:
        """Disable the schedule."""
        self.enabled = False

    @property
    def is_due(self) -> bool:
        """Return True if the schedule is ready to run."""
        return self.enabled and datetime.now(UTC) >= self.next_run
