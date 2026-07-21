"""
Unit tests for ai.workflow_status.
"""

from ai.workflow_status import WorkflowStatus


def test_pending_state() -> None:
    status = WorkflowStatus.PENDING

    assert status.is_active
    assert status.can_execute
    assert not status.is_finished


def test_running_state() -> None:
    status = WorkflowStatus.RUNNING

    assert status.is_active
    assert status.can_execute
    assert not status.is_finished


def test_paused_state() -> None:
    status = WorkflowStatus.PAUSED

    assert status.is_active
    assert not status.can_execute
    assert not status.is_finished


def test_completed_state() -> None:
    status = WorkflowStatus.COMPLETED

    assert status.is_finished
    assert not status.is_active
    assert not status.can_execute


def test_failed_state() -> None:
    status = WorkflowStatus.FAILED

    assert status.is_finished
    assert not status.is_active
    assert not status.can_execute


def test_cancelled_state() -> None:
    status = WorkflowStatus.CANCELLED

    assert status.is_finished
    assert not status.is_active
    assert not status.can_execute
