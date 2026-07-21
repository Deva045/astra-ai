"""
Event handler definitions for Astra AI.
"""

from __future__ import annotations

from typing import Protocol

from ai.event import Event


class EventHandler(Protocol):
    """Protocol for event handlers."""

    def __call__(self, event: Event) -> None:
        """
        Handle an event.

        Parameters
        ----------
        event:
            The event being dispatched.
        """
        ...
