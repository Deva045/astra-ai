"""
Unit tests for ai.task_manager.
"""

from ai.task_manager import TaskManager
from ai.task_status import TaskStatus


def test_create_task() -> None:
    manager = TaskManager()

    task = manager.create_task("Demo")

    assert task.name == "Demo"
    assert manager.task_count == 1


def test_get_task() -> None:
    manager = TaskManager()

    task = manager.create_task("Demo")

    assert manager.get_task(task.task_id) is task


def test_remove_task() -> None:
    manager = TaskManager()

    task = manager.create_task("Demo")

    assert manager.remove_task(task.task_id) is True
    assert manager.task_count == 0


def test_start_pause_resume() -> None:
    manager = TaskManager()

    task = manager.create_task("Demo")

    manager.start_task(task.task_id)
    assert task.status == TaskStatus.RUNNING

    manager.pause_task(task.task_id)
    assert task.status == TaskStatus.PAUSED

    manager.resume_task(task.task_id)
    assert task.status == TaskStatus.RUNNING


def test_complete_task() -> None:
    manager = TaskManager()

    task = manager.create_task("Demo")

    manager.complete_task(task.task_id)

    assert task.status == TaskStatus.COMPLETED
    assert task.progress == 100


def test_fail_task() -> None:
    manager = TaskManager()

    task = manager.create_task("Demo")

    manager.fail_task(task.task_id, "error")

    assert task.status == TaskStatus.FAILED
    assert task.error == "error"


def test_cancel_task() -> None:
    manager = TaskManager()

    task = manager.create_task("Demo")

    manager.cancel_task(task.task_id)

    assert task.status == TaskStatus.CANCELLED


def test_update_progress() -> None:
    manager = TaskManager()

    task = manager.create_task("Demo")

    manager.update_progress(task.task_id, 55)

    assert task.progress == 55


def test_active_tasks() -> None:
    manager = TaskManager()

    task = manager.create_task("Demo")

    assert len(manager.active_tasks) == 1

    manager.complete_task(task.task_id)

    assert len(manager.active_tasks) == 0


def test_completed_tasks() -> None:
    manager = TaskManager()

    task = manager.create_task("Demo")

    manager.complete_task(task.task_id)

    assert len(manager.completed_tasks) == 1
    assert manager.completed_tasks[0] is task


def test_clear_tasks() -> None:
    manager = TaskManager()

    manager.create_task("A")
    manager.create_task("B")

    assert manager.task_count == 2

    manager.clear()

    assert manager.task_count == 0
