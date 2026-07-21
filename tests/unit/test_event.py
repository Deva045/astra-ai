"""
Unit tests for ai.event.
"""

from ai.event import Event


def test_default_event() -> None:
    event = Event(
        event_id="evt-1",
        event_type="message",
        source="assistant",
    )

    assert event.event_id == "evt-1"
    assert event.event_type == "message"
    assert event.source == "assistant"
    assert event.payload == {}
    assert event.timestamp is not None


def test_add_data() -> None:
    event = Event(
        event_id="evt-1",
        event_type="message",
        source="assistant",
    )

    event.add_data("text", "hello")
    event.add_data("count", 1)

    assert event.payload["text"] == "hello"
    assert event.payload["count"] == 1


def test_get_data() -> None:
    event = Event(
        event_id="evt-1",
        event_type="message",
        source="assistant",
        payload={"value": 123},
    )

    assert event.get_data("value") == 123
    assert event.get_data("missing") is None
    assert event.get_data("missing", "default") == "default"
