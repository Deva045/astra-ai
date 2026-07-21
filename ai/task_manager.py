"""
Task manager for Astra AI.

Provides in-memory task management functionality including
creation, lookup, lifecycle operations, and progress updates.
"""

from __future__ import annotations

from uuid import uuid4

from ai.task import Task
from ai.task_status import TaskStatus


class TaskManager:
    """Manages the lifecycle of tasks."""

    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def create_task(self, task: Task | str, description: str = "") -> Task:
        """Register an existing task or create a new one."""
        if isinstance(task, Task):
            self._tasks[task.task_id] = task
            return task

        new_task = Task(
            task_id=str(uuid4()),
            name=task,
            description=description,
        )
        self._tasks[new_task.task_id] = new_task
        return new_task

    def get_task(self, task_id: str) -> Task | None:
        """Return a task by ID."""
        return self._tasks.get(task_id)

    def list_tasks(self) -> list[Task]:
        """Return all registered tasks."""
        return list(self._tasks.values())

    def remove_task(self, task_id: str) -> bool:
        """Remove a task."""
        return self._tasks.pop(task_id, None) is not None

    def start_task(self, task_id: str) -> bool:
        task = self.get_task(task_id)
        if task is None:
            return False
        task.start()
        return True

    def pause_task(self, task_id: str) -> bool:
        task = self.get_task(task_id)
        if task is None:
            return False
        task.pause()
        return True

    def resume_task(self, task_id: str) -> bool:
        task = self.get_task(task_id)
        if task is None:
            return False
        task.resume()
        return True

    def complete_task(self, task_id: str) -> bool:
        task = self.get_task(task_id)
        if task is None:
            return False
        task.complete()
        return True

    def fail_task(self, task_id: str, reason: str = "") -> bool:
        task = self.get_task(task_id)
        if task is None:
            return False
        task.fail(reason)
        return True

    def cancel_task(self, task_id: str) -> bool:
        task = self.get_task(task_id)
        if task is None:
            return False
        task.cancel()
        return True

    def update_progress(self, task_id: str, progress: int) -> bool:
        task = self.get_task(task_id)
        if task is None:
            return False
        task.update_progress(progress)
        return True

    def clear(self) -> None:
        """Remove all tasks."""
        self._tasks.clear()

    @property
    def task_count(self) -> int:
        """Return the total number of tasks."""
        return len(self._tasks)

    @property
    def active_tasks(self) -> list[Task]:
        """Return all non-terminal tasks."""
        return [
            task
            for task in self._tasks.values()
            if task.status in (
                TaskStatus.PENDING,
                TaskStatus.RUNNING,
                TaskStatus.PAUSED,
            )
        ]

    @property
    def completed_tasks(self) -> list[Task]:
        """Return all completed tasks."""
        return [
            task
            for task in self._tasks.values()
            if task.status == TaskStatus.COMPLETED
        ]
