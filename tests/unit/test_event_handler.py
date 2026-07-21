"""
Unit tests for ai.event_handler.
"""

from ai.event import Event
from ai.event_handler import EventHandler


class SampleHandler:
    """Simple event handler implementation."""

    def __call__(self, event: Event) -> None:
        event.add_data("handled", True)


def test_handler_invocation() -> None:
    handler = SampleHandler()

    event = Event(
        event_id="evt-1",
        event_type="message",
        source="test",
    )

    handler(event)

    assert event.get_data("handled") is True


def test_protocol_type() -> None:
    handler: EventHandler = SampleHandler()

    event = Event(
        event_id="evt-2",
        event_type="message",
        source="test",
    )

    handler(event)

    assert event.get_data("handled") is True
