"""
Unit tests for ai.workflow.
"""

from ai.workflow import Workflow
from ai.workflow_status import WorkflowStatus
from ai.workflow_step import WorkflowStep


def test_default_workflow() -> None:
    workflow = Workflow(
        workflow_id="wf-1",
        name="Example Workflow",
    )

    assert workflow.workflow_id == "wf-1"
    assert workflow.name == "Example Workflow"
    assert workflow.status == WorkflowStatus.PENDING
    assert workflow.total_steps == 0
    assert workflow.completed_steps == 0
    assert workflow.progress == 0.0


def test_add_steps() -> None:
    workflow = Workflow(
        workflow_id="wf-1",
        name="Workflow",
    )

    workflow.add_step(WorkflowStep("1", "Step 1"))
    workflow.add_step(WorkflowStep("2", "Step 2"))

    assert workflow.total_steps == 2
    assert workflow.completed_steps == 0
    assert workflow.progress == 0.0


def test_progress_updates() -> None:
    workflow = Workflow(
        workflow_id="wf-1",
        name="Workflow",
    )

    step1 = WorkflowStep("1", "Step 1")
    step2 = WorkflowStep("2", "Step 2")

    workflow.add_step(step1)
    workflow.add_step(step2)

    step1.complete()

    assert workflow.completed_steps == 1
    assert workflow.progress == 50.0

    step2.complete()

    assert workflow.completed_steps == 2
    assert workflow.progress == 100.0


def test_workflow_lifecycle() -> None:
    workflow = Workflow(
        workflow_id="wf-1",
        name="Workflow",
    )

    workflow.start()
    assert workflow.status == WorkflowStatus.RUNNING
    assert workflow.started_at is not None

    workflow.complete()
    assert workflow.status == WorkflowStatus.COMPLETED
    assert workflow.completed_at is not None


def test_fail_workflow() -> None:
    workflow = Workflow(
        workflow_id="wf-1",
        name="Workflow",
    )

    workflow.fail()

    assert workflow.status == WorkflowStatus.FAILED
    assert workflow.completed_at is not None


def test_cancel_workflow() -> None:
    workflow = Workflow(
        workflow_id="wf-1",
        name="Workflow",
    )

    workflow.cancel()

    assert workflow.status == WorkflowStatus.CANCELLED
    assert workflow.completed_at is not None
