
"""
Tests for execution plans.
"""

from ai.plan import Plan
from ai.plan_status import PlanStatus
from ai.plan_step import PlanStep


def create_step(
    step_id: int,
    title: str,
    status: PlanStatus = PlanStatus.PENDING,
) -> PlanStep:
    """
    Helper for creating plan steps.
    """
    return PlanStep(
        id=step_id,
        title=title,
        description="",
        status=status,
    )


def test_empty_plan():
    """
    Empty plan should report no steps.
    """
    plan = Plan(goal="Test")

    assert plan.step_count() == 0
    assert not plan.has_steps()
    assert plan.progress() == 0.0
    assert plan.next_step() is None
    assert plan.remaining_steps() == 0
    assert not plan.is_complete()


def test_add_step():
    """
    Adding a step should update the plan.
    """
    plan = Plan(goal="Test")

    plan.add_step(
        create_step(
            1,
            "Step One",
        )
    )

    assert plan.step_count() == 1
    assert plan.has_steps()
    assert plan.remaining_steps() == 1
    assert plan.next_step() is not None


def test_progress_partial():
    """
    Progress should reflect completed steps.
    """
    plan = Plan(goal="Test")

    plan.add_step(
        create_step(
            1,
            "Done",
            PlanStatus.COMPLETED,
        )
    )

    plan.add_step(
        create_step(
            2,
            "Pending",
        )
    )

    assert plan.progress() == 50.0
    assert plan.remaining_steps() == 1


def test_progress_complete():
    """
    Fully completed plan.
    """
    plan = Plan(goal="Test")

    plan.add_step(
        create_step(
            1,
            "One",
            PlanStatus.COMPLETED,
        )
    )

    plan.add_step(
        create_step(
            2,
            "Two",
            PlanStatus.COMPLETED,
        )
    )

    assert plan.progress() == 100.0
    assert plan.remaining_steps() == 0
    assert plan.next_step() is None
    assert plan.is_complete()


def test_next_step():
    """
    Next pending step should be returned.
    """
    plan = Plan(goal="Test")

    plan.add_step(
        create_step(
            1,
            "Done",
            PlanStatus.COMPLETED,
        )
    )

    second = create_step(
        2,
        "Pending",
    )

    plan.add_step(second)

    assert plan.next_step() == second
