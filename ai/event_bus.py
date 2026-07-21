"""
Event bus implementation for Astra AI.
"""

from __future__ import annotations

from collections import defaultdict

from ai.event import Event
from ai.event_handler import EventHandler


class EventBus:
    """Simple publish/subscribe event bus."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Register a handler for an event type."""
        self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: EventHandler) -> bool:
        """Remove a handler from an event type."""
        handlers = self._handlers.get(event_type)

        if handlers is None:
            return False

        try:
            handlers.remove(handler)
        except ValueError:
            return False

        if not handlers:
            del self._handlers[event_type]

        return True

    def publish(self, event: Event) -> int:
        """
        Publish an event.

        Returns the number of handlers invoked.
        """
        handlers = self._handlers.get(event.event_type, [])

        for handler in handlers:
            handler(event)

        return len(handlers)

    def clear(self) -> None:
        """Remove all subscriptions."""
        self._handlers.clear()

    @property
    def subscription_count(self) -> int:
        """Return the total number of registered handlers."""
        return sum(len(handlers) for handlers in self._handlers.values())
