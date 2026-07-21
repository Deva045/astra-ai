"""
Task executor for Astra AI.

Coordinates task execution using the TaskManager, TaskQueue,
ExecutionMonitor, and RecoveryEngine.
"""

from __future__ import annotations

from ai.execution_monitor import ExecutionMonitor
from ai.recovery_engine import RecoveryEngine
from ai.task import Task
from ai.task_manager import TaskManager
from ai.task_queue import TaskQueue


class TaskExecutor:
    """Executes queued tasks."""

    def __init__(
        self,
        manager: TaskManager | None = None,
        queue: TaskQueue | None = None,
        monitor: ExecutionMonitor | None = None,
        recovery: RecoveryEngine | None = None,
    ) -> None:
        self.manager = manager or TaskManager()
        self.queue = queue or TaskQueue()
        self.monitor = monitor or ExecutionMonitor()
        self.recovery = recovery or RecoveryEngine()

    def submit(self, task: Task) -> None:
        """Register and queue a task."""
        self.manager.create_task(task)
        self.queue.enqueue(task)

    def execute_next(self) -> bool:
        """Execute the next task in the queue."""
        task = self.queue.dequeue()

        if task is None:
            return False

        self.manager.start_task(task.task_id)
        self.monitor.start(task.name, 1)

        def operation() -> None:
            self.monitor.update_step(1, task.name)

        success = self.recovery.run(operation)

        if success:
            self.manager.complete_task(task.task_id)
            self.monitor.complete()
        else:
            self.manager.fail_task(
                task.task_id,
                self.recovery.last_error or "Execution failed",
            )
            self.monitor.fail(
                self.recovery.last_error or "Execution failed",
            )

        return success

    @property
    def pending_tasks(self) -> int:
        """Return the number of queued tasks."""
        return self.queue.size

    def clear(self) -> None:
        """Clear all executor state."""
        self.queue.clear()
        self.manager.clear()
        self.monitor.reset()
        self.recovery.reset()
