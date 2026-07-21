"""
Unit tests for ai.scheduler.
"""

from datetime import UTC, datetime, timedelta

from ai.schedule import Schedule
from ai.scheduler import Scheduler


def test_register_and_get_schedule() -> None:
    scheduler = Scheduler()

    schedule = Schedule(
        schedule_id="sch-1",
        name="Example",
        interval=timedelta(minutes=5),
    )

    scheduler.register(schedule)

    assert scheduler.schedule_count == 1
    assert scheduler.get("sch-1") is schedule


def test_remove_schedule() -> None:
    scheduler = Scheduler()

    schedule = Schedule(
        schedule_id="sch-1",
        name="Example",
        interval=timedelta(minutes=5),
    )

    scheduler.register(schedule)

    assert scheduler.remove("sch-1") is True
    assert scheduler.get("sch-1") is None
    assert scheduler.schedule_count == 0


def test_clear_schedules() -> None:
    scheduler = Scheduler()

    scheduler.register(Schedule("1", "A", timedelta(minutes=1)))
    scheduler.register(Schedule("2", "B", timedelta(minutes=2)))

    assert scheduler.schedule_count == 2

    scheduler.clear()

    assert scheduler.schedule_count == 0
    assert scheduler.schedules == []


def test_due_schedules() -> None:
    scheduler = Scheduler()

    schedule = Schedule(
        schedule_id="sch-1",
        name="Example",
        interval=timedelta(minutes=5),
    )

    schedule.next_run = datetime.now(UTC) - timedelta(seconds=1)

    scheduler.register(schedule)

    due = scheduler.due_schedules()

    assert len(due) == 1
    assert due[0] is schedule


def test_run_due() -> None:
    scheduler = Scheduler()

    schedule = Schedule(
        schedule_id="sch-1",
        name="Example",
        interval=timedelta(minutes=5),
    )

    schedule.next_run = datetime.now(UTC) - timedelta(seconds=1)

    scheduler.register(schedule)

    assert scheduler.run_due() == 1
    assert schedule.last_run is not None
    assert schedule.next_run > schedule.last_run


def test_schedules_property() -> None:
    scheduler = Scheduler()

    s1 = Schedule("1", "A", timedelta(minutes=1))
    s2 = Schedule("2", "B", timedelta(minutes=2))

    scheduler.register(s1)
    scheduler.register(s2)

    schedules = scheduler.schedules

    assert len(schedules) == 2
    assert s1 in schedules
    assert s2 in schedules
