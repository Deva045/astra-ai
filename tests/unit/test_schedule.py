"""
Unit tests for ai.schedule.
"""

from datetime import UTC, datetime, timedelta

from ai.schedule import Schedule


def test_default_schedule() -> None:
    schedule = Schedule(
        schedule_id="sch-1",
        name="Example",
        interval=timedelta(minutes=5),
    )

    assert schedule.schedule_id == "sch-1"
    assert schedule.name == "Example"
    assert schedule.enabled is True
    assert schedule.last_run is None


def test_mark_executed() -> None:
    schedule = Schedule(
        schedule_id="sch-1",
        name="Example",
        interval=timedelta(minutes=10),
    )

    schedule.mark_executed()

    assert schedule.last_run is not None
    assert schedule.next_run > schedule.last_run


def test_enable_disable() -> None:
    schedule = Schedule(
        schedule_id="sch-1",
        name="Example",
        interval=timedelta(minutes=1),
    )

    schedule.disable()
    assert schedule.enabled is False

    schedule.enable()
    assert schedule.enabled is True


def test_is_due() -> None:
    schedule = Schedule(
        schedule_id="sch-1",
        name="Example",
        interval=timedelta(minutes=5),
    )

    schedule.next_run = datetime.now(UTC) - timedelta(seconds=1)

    assert schedule.is_due is True


def test_is_not_due_when_disabled() -> None:
    schedule = Schedule(
        schedule_id="sch-1",
        name="Example",
        interval=timedelta(minutes=5),
    )

    schedule.disable()
    schedule.next_run = datetime.now(UTC) - timedelta(minutes=1)

    assert schedule.is_due is False
