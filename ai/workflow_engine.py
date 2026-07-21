"""
Workflow execution engine for Astra AI.
"""

from __future__ import annotations

from ai.workflow import Workflow


class WorkflowEngine:
    """Executes and manages workflows."""

    def __init__(self) -> None:
        self._workflows: dict[str, Workflow] = {}

    def register(self, workflow: Workflow) -> None:
        """Register a workflow."""
        self._workflows[workflow.workflow_id] = workflow

    def get(self, workflow_id: str) -> Workflow | None:
        """Return a workflow by ID."""
        return self._workflows.get(workflow_id)

    def execute(self, workflow_id: str) -> bool:
        """
        Execute a workflow.

        Each step is completed sequentially. If all steps complete,
        the workflow is marked as completed.
        """
        workflow = self.get(workflow_id)

        if workflow is None:
            return False

        workflow.start()

        try:
            for step in workflow.steps:
                step.complete()

            workflow.complete()
            return True

        except Exception:
            workflow.fail()
            return False

    def remove(self, workflow_id: str) -> bool:
        """Remove a workflow."""
        return self._workflows.pop(workflow_id, None) is not None

    def clear(self) -> None:
        """Remove all workflows."""
        self._workflows.clear()

    @property
    def workflow_count(self) -> int:
        """Return the number of registered workflows."""
        return len(self._workflows)

    @property
    def workflows(self) -> list[Workflow]:
        """Return all registered workflows."""
        return list(self._workflows.values())
