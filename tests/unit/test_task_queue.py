"""
Unit tests for ai.task_queue.
"""

from ai.task import Task
from ai.task_queue import TaskQueue


def create_task(name: str) -> Task:
    return Task(task_id=name, name=name)


def test_queue_is_empty_initially() -> None:
    queue = TaskQueue()

    assert queue.is_empty
    assert queue.size == 0
    assert len(queue) == 0


def test_enqueue_single_task() -> None:
    queue = TaskQueue()
    task = create_task("A")

    queue.enqueue(task)

    assert not queue.is_empty
    assert queue.size == 1
    assert queue.peek() is task


def test_fifo_order() -> None:
    queue = TaskQueue()

    task1 = create_task("A")
    task2 = create_task("B")
    task3 = create_task("C")

    queue.enqueue(task1)
    queue.enqueue(task2)
    queue.enqueue(task3)

    assert queue.dequeue() is task1
    assert queue.dequeue() is task2
    assert queue.dequeue() is task3
    assert queue.dequeue() is None


def test_peek_does_not_remove() -> None:
    queue = TaskQueue()

    task = create_task("Demo")

    queue.enqueue(task)

    assert queue.peek() is task
    assert queue.size == 1


def test_remove_task() -> None:
    queue = TaskQueue()

    task = create_task("Demo")

    queue.enqueue(task)

    assert queue.remove(task)
    assert queue.is_empty


def test_remove_missing_task() -> None:
    queue = TaskQueue()

    assert not queue.remove(create_task("Missing"))


def test_clear_queue() -> None:
    queue = TaskQueue()

    queue.enqueue(create_task("A"))
    queue.enqueue(create_task("B"))

    queue.clear()

    assert queue.is_empty
    assert queue.size == 0


def test_iter_queue() -> None:
    queue = TaskQueue()

    queue.enqueue(create_task("A"))
    queue.enqueue(create_task("B"))

    names = [task.name for task in queue]

    assert names == ["A", "B"]


def test_len_queue() -> None:
    queue = TaskQueue()

    queue.enqueue(create_task("A"))
    queue.enqueue(create_task("B"))
    queue.enqueue(create_task("C"))

    assert len(queue) == 3
