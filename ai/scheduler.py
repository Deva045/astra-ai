"""
Scheduler engine for Astra AI.
"""

from __future__ import annotations

from ai.schedule import Schedule


class Scheduler:
    """Manages registered schedules."""

    def __init__(self) -> None:
        self._schedules: dict[str, Schedule] = {}

    def register(self, schedule: Schedule) -> None:
        """Register a schedule."""
        self._schedules[schedule.schedule_id] = schedule

    def get(self, schedule_id: str) -> Schedule | None:
        """Return a schedule by ID."""
        return self._schedules.get(schedule_id)

    def remove(self, schedule_id: str) -> bool:
        """Remove a schedule."""
        return self._schedules.pop(schedule_id, None) is not None

    def clear(self) -> None:
        """Remove all schedules."""
        self._schedules.clear()

    def due_schedules(self) -> list[Schedule]:
        """Return all schedules that are ready to run."""
        return [
            schedule
            for schedule in self._schedules.values()
            if schedule.is_due
        ]

    def run_due(self) -> int:
        """
        Execute all due schedules.

        Returns the number of schedules executed.
        """
        count = 0

        for schedule in self.due_schedules():
            schedule.mark_executed()
            count += 1

        return count

    @property
    def schedule_count(self) -> int:
        """Return the number of registered schedules."""
        return len(self._schedules)

    @property
    def schedules(self) -> list[Schedule]:
        """Return all registered schedules."""
        return list(self._schedules.values())
