"""
Unit tests for ai.workflow_step.
"""

from ai.workflow_step import WorkflowStep


def test_default_step() -> None:
    step = WorkflowStep(
        step_id="step-1",
        name="Test Step",
    )

    assert step.step_id == "step-1"
    assert step.name == "Test Step"
    assert step.description == ""
    assert step.completed is False
    assert step.metadata == {}


def test_complete_step() -> None:
    step = WorkflowStep(
        step_id="step-1",
        name="Example",
    )

    step.complete()

    assert step.completed is True


def test_reset_step() -> None:
    step = WorkflowStep(
        step_id="step-1",
        name="Example",
    )

    step.complete()
    assert step.completed is True

    step.reset()

    assert step.completed is False


def test_metadata_storage() -> None:
    step = WorkflowStep(
        step_id="step-1",
        name="Example",
        metadata={
            "priority": "high",
            "retries": 3,
        },
    )

    assert step.metadata["priority"] == "high"
    assert step.metadata["retries"] == 3
