"""
Unit tests for ai.task.
"""

from ai.task import Task
from ai.task_status import TaskStatus


def test_task_defaults() -> None:
    task = Task(task_id="1", name="Demo Task")

    assert task.task_id == "1"
    assert task.name == "Demo Task"
    assert task.description == ""
    assert task.status == TaskStatus.PENDING
    assert task.progress == 0
    assert not task.is_finished


def test_start_task() -> None:
    task = Task(task_id="1", name="Demo")

    task.start()

    assert task.status == TaskStatus.RUNNING
    assert task.started_at is not None


def test_pause_resume_task() -> None:
    task = Task(task_id="1", name="Demo")

    task.start()
    task.pause()

    assert task.status == TaskStatus.PAUSED

    task.resume()

    assert task.status == TaskStatus.RUNNING


def test_update_progress() -> None:
    task = Task(task_id="1", name="Demo")

    task.update_progress(45)
    assert task.progress == 45

    task.update_progress(150)
    assert task.progress == 100

    task.update_progress(-5)
    assert task.progress == 0


def test_complete_task() -> None:
    task = Task(task_id="1", name="Demo")

    task.complete()

    assert task.status == TaskStatus.COMPLETED
    assert task.progress == 100
    assert task.completed_at is not None
    assert task.is_finished


def test_fail_task() -> None:
    task = Task(task_id="1", name="Demo")

    task.fail("failure")

    assert task.status == TaskStatus.FAILED
    assert task.error == "failure"
    assert task.completed_at is not None
    assert task.is_finished


def test_cancel_task() -> None:
    task = Task(task_id="1", name="Demo")

    task.cancel()

    assert task.status == TaskStatus.CANCELLED
    assert task.completed_at is not None
    assert task.is_finished
