"""
Task queue for Astra AI.

Provides a simple FIFO queue for Task objects.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterator

from ai.task import Task


class TaskQueue:
    """FIFO queue for Task instances."""

    def __init__(self) -> None:
        self._queue: deque[Task] = deque()

    def enqueue(self, task: Task) -> None:
        """Add a task to the end of the queue."""
        self._queue.append(task)

    def dequeue(self) -> Task | None:
        """Remove and return the next task."""
        if not self._queue:
            return None
        return self._queue.popleft()

    def peek(self) -> Task | None:
        """Return the next task without removing it."""
        if not self._queue:
            return None
        return self._queue[0]

    def remove(self, task: Task) -> bool:
        """Remove a specific task from the queue."""
        try:
            self._queue.remove(task)
            return True
        except ValueError:
            return False

    def clear(self) -> None:
        """Remove all queued tasks."""
        self._queue.clear()

    @property
    def is_empty(self) -> bool:
        """Return True if the queue is empty."""
        return len(self._queue) == 0

    @property
    def size(self) -> int:
        """Return the number of queued tasks."""
        return len(self._queue)

    def __len__(self) -> int:
        return len(self._queue)

    def __iter__(self) -> Iterator[Task]:
        return iter(self._queue)
