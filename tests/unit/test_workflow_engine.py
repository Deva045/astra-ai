"""
Unit tests for ai.workflow_engine.
"""

from ai.workflow import Workflow
from ai.workflow_engine import WorkflowEngine
from ai.workflow_status import WorkflowStatus
from ai.workflow_step import WorkflowStep


def test_register_and_get_workflow() -> None:
    engine = WorkflowEngine()

    workflow = Workflow(
        workflow_id="wf-1",
        name="Workflow",
    )

    engine.register(workflow)

    assert engine.workflow_count == 1
    assert engine.get("wf-1") is workflow


def test_remove_workflow() -> None:
    engine = WorkflowEngine()

    workflow = Workflow(
        workflow_id="wf-1",
        name="Workflow",
    )

    engine.register(workflow)

    assert engine.remove("wf-1") is True
    assert engine.workflow_count == 0
    assert engine.get("wf-1") is None


def test_clear_workflows() -> None:
    engine = WorkflowEngine()

    engine.register(Workflow("1", "A"))
    engine.register(Workflow("2", "B"))

    assert engine.workflow_count == 2

    engine.clear()

    assert engine.workflow_count == 0
    assert engine.workflows == []


def test_execute_workflow() -> None:
    engine = WorkflowEngine()

    workflow = Workflow(
        workflow_id="wf-1",
        name="Workflow",
    )

    workflow.add_step(WorkflowStep("1", "Step 1"))
    workflow.add_step(WorkflowStep("2", "Step 2"))

    engine.register(workflow)

    assert engine.execute("wf-1") is True
    assert workflow.status == WorkflowStatus.COMPLETED
    assert workflow.progress == 100.0

    assert all(step.completed for step in workflow.steps)


def test_execute_missing_workflow() -> None:
    engine = WorkflowEngine()

    assert engine.execute("missing") is False


def test_workflows_property() -> None:
    engine = WorkflowEngine()

    w1 = Workflow("1", "Workflow 1")
    w2 = Workflow("2", "Workflow 2")

    engine.register(w1)
    engine.register(w2)

    workflows = engine.workflows

    assert len(workflows) == 2
    assert w1 in workflows
    assert w2 in workflows
