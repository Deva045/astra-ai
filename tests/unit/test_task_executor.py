"""
Unit tests for ai.task_executor.
"""

from ai.task import Task
from ai.task_executor import TaskExecutor
from ai.task_status import TaskStatus


def create_task(task_id: str = "task1") -> Task:
    return Task(
        task_id=task_id,
        name=f"Task {task_id}",
        description="Test task",
    )


def test_executor_initial_state() -> None:
    executor = TaskExecutor()

    assert executor.pending_tasks == 0


def test_submit_task() -> None:
    executor = TaskExecutor()

    task = create_task()

    executor.submit(task)

    assert executor.pending_tasks == 1
    assert executor.manager.task_count == 1


def test_execute_single_task() -> None:
    executor = TaskExecutor()

    task = create_task()

    executor.submit(task)

    assert executor.execute_next()

    stored = executor.manager.get_task(task.task_id)

    assert stored is not None
    assert stored.status == TaskStatus.COMPLETED
    assert executor.pending_tasks == 0
    assert executor.monitor.successful


def test_execute_empty_queue() -> None:
    executor = TaskExecutor()

    assert not executor.execute_next()


def test_multiple_tasks_fifo() -> None:
    executor = TaskExecutor()

    task1 = create_task("one")
    task2 = create_task("two")

    executor.submit(task1)
    executor.submit(task2)

    assert executor.execute_next()
    assert executor.manager.get_task("one").status == TaskStatus.COMPLETED

    assert executor.execute_next()
    assert executor.manager.get_task("two").status == TaskStatus.COMPLETED

    assert executor.pending_tasks == 0


def test_clear_executor() -> None:
    executor = TaskExecutor()

    executor.submit(create_task())

    executor.clear()

    assert executor.pending_tasks == 0
    assert executor.manager.task_count == 0
    assert executor.monitor.task_name == ""
    assert executor.recovery.retry_count == 0


def test_monitor_updates() -> None:
    executor = TaskExecutor()

    task = create_task()

    executor.submit(task)
    executor.execute_next()

    assert executor.monitor.progress == 100.0
    assert executor.monitor.successful


def test_recovery_reset_after_clear() -> None:
    executor = TaskExecutor()

    executor.recovery.record_failure("Error")

    executor.clear()

    assert executor.recovery.retry_count == 0
    assert executor.recovery.last_error is None


def test_submit_multiple_tasks() -> None:
    executor = TaskExecutor()

    for i in range(5):
        executor.submit(create_task(str(i)))

    assert executor.pending_tasks == 5
    assert executor.manager.task_count == 5
