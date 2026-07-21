"""
Unit tests for ai.execution_monitor.
"""

from time import sleep

from ai.execution_monitor import ExecutionMonitor


def test_initial_state() -> None:
    monitor = ExecutionMonitor()

    assert monitor.task_name == ""
    assert monitor.total_steps == 0
    assert monitor.completed_steps == 0
    assert monitor.progress == 0.0
    assert monitor.duration is None
    assert not monitor.running
    assert not monitor.successful


def test_start_monitor() -> None:
    monitor = ExecutionMonitor()

    monitor.start("Demo Task", 5)

    assert monitor.task_name == "Demo Task"
    assert monitor.total_steps == 5
    assert monitor.completed_steps == 0
    assert monitor.running
    assert not monitor.successful
    assert monitor.started_at is not None


def test_update_step() -> None:
    monitor = ExecutionMonitor()

    monitor.start("Demo", 4)
    monitor.update_step(2, "Halfway")

    assert monitor.completed_steps == 2
    assert monitor.current_step == "Halfway"
    assert monitor.progress == 50.0


def test_complete() -> None:
    monitor = ExecutionMonitor()

    monitor.start("Demo", 3)
    monitor.complete()

    assert monitor.successful
    assert not monitor.running
    assert monitor.completed_steps == 3
    assert monitor.finished_at is not None
    assert monitor.progress == 100.0


def test_fail() -> None:
    monitor = ExecutionMonitor()

    monitor.start("Demo", 2)
    monitor.fail("Something went wrong")

    assert not monitor.running
    assert not monitor.successful
    assert monitor.error == "Something went wrong"
    assert monitor.finished_at is not None


def test_reset() -> None:
    monitor = ExecutionMonitor()

    monitor.start("Demo", 5)
    monitor.update_step(2, "Working")
    monitor.reset()

    assert monitor.task_name == ""
    assert monitor.total_steps == 0
    assert monitor.completed_steps == 0
    assert monitor.current_step == ""
    assert monitor.started_at is None
    assert monitor.finished_at is None
    assert monitor.error is None
    assert not monitor.running
    assert not monitor.successful


def test_duration() -> None:
    monitor = ExecutionMonitor()

    monitor.start("Demo", 1)
    sleep(0.01)
    monitor.complete()

    assert monitor.duration is not None
    assert monitor.duration >= 0


def test_progress_limits() -> None:
    monitor = ExecutionMonitor()

    monitor.start("Demo", 5)
    monitor.update_step(10, "Done")

    assert monitor.completed_steps == 5
    assert monitor.progress == 100.0


def test_zero_steps_progress() -> None:
    monitor = ExecutionMonitor()

    monitor.start("Empty", 0)

    assert monitor.progress == 0.0
