"""
Unit tests for ai.event_bus.
"""

from ai.event import Event
from ai.event_bus import EventBus


def test_subscribe_and_publish() -> None:
    bus = EventBus()
    received: list[Event] = []

    def handler(event: Event) -> None:
        received.append(event)

    bus.subscribe("message", handler)

    event = Event(
        event_id="evt-1",
        event_type="message",
        source="test",
    )

    count = bus.publish(event)

    assert count == 1
    assert received == [event]
    assert bus.subscription_count == 1


def test_unsubscribe() -> None:
    bus = EventBus()

    def handler(event: Event) -> None:
        pass

    bus.subscribe("message", handler)

    assert bus.unsubscribe("message", handler) is True
    assert bus.subscription_count == 0
    assert bus.unsubscribe("message", handler) is False


def test_publish_without_handlers() -> None:
    bus = EventBus()

    event = Event(
        event_id="evt-2",
        event_type="missing",
        source="test",
    )

    assert bus.publish(event) == 0


def test_clear() -> None:
    bus = EventBus()

    def handler(event: Event) -> None:
        pass

    bus.subscribe("a", handler)
    bus.subscribe("b", handler)

    assert bus.subscription_count == 2

    bus.clear()

    assert bus.subscription_count == 0


def test_multiple_handlers() -> None:
    bus = EventBus()

    calls: list[int] = []

    def handler1(event: Event) -> None:
        calls.append(1)

    def handler2(event: Event) -> None:
        calls.append(2)

    bus.subscribe("message", handler1)
    bus.subscribe("message", handler2)

    event = Event(
        event_id="evt-3",
        event_type="message",
        source="test",
    )

    assert bus.publish(event) == 2
    assert calls == [1, 2]
