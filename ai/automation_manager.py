"""
Automation manager for Astra AI.
"""

from __future__ import annotations

from ai.automation import Automation


class AutomationManager:
    """Manages registered automations."""

    def __init__(self) -> None:
        self._automations: dict[str, Automation] = {}

    def register(self, automation: Automation) -> None:
        """Register an automation."""
        self._automations[automation.automation_id] = automation

    def unregister(self, automation_id: str) -> bool:
        """Remove an automation by ID."""
        return self._automations.pop(automation_id, None) is not None

    def get(self, automation_id: str) -> Automation | None:
        """Return an automation by ID."""
        return self._automations.get(automation_id)

    def all_automations(self) -> list[Automation]:
        """Return all registered automations."""
        return list(self._automations.values())

    def enabled_automations(self) -> list[Automation]:
        """Return all enabled automations."""
        return [
            automation
            for automation in self._automations.values()
            if automation.enabled
        ]

    def clear(self) -> None:
        """Remove all registered automations."""
        self._automations.clear()

    @property
    def count(self) -> int:
        """Return the number of registered automations."""
        return len(self._automations)
