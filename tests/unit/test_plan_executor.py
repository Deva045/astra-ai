
"""
Tests for the PlanExecutor.
"""

from ai.plan import Plan
from ai.plan_executor import PlanExecutor
from ai.plan_status import PlanStatus
from ai.plan_step import PlanStep


class DummyToolRouter:
    """
    Simple ToolRouter stub used for testing.
    """

    def __init__(self) -> None:
        self.calls: list[str] = []

    def route(
        self,
        text: str,
    ) -> str:
        self.calls.append(text)
        return "ok"


def create_step(
    step_id: int,
    title: str,
    status: PlanStatus = PlanStatus.PENDING,
) -> PlanStep:
    return PlanStep(
        id=step_id,
        title=title,
        description="",
        status=status,
    )


def test_can_execute_empty():
    executor = PlanExecutor()
    plan = Plan(goal="Test")

    assert not executor.can_execute(plan)


def test_can_execute_pending():
    executor = PlanExecutor()
    plan = Plan(goal="Test")

    plan.add_step(
        create_step(
            1,
            "Step",
        )
    )

    assert executor.can_execute(plan)


def test_execute_single_step():
    executor = PlanExecutor()

    plan = Plan(goal="Test")

    step = create_step(
        1,
        "Step",
    )

    plan.add_step(step)

    executor.execute(plan)

    assert step.status == PlanStatus.COMPLETED
    assert plan.is_complete()


def test_execute_multiple_steps():
    executor = PlanExecutor()

    plan = Plan(goal="Test")

    plan.add_step(
        create_step(
            1,
            "One",
        )
    )

    plan.add_step(
        create_step(
            2,
            "Two",
        )
    )

    executor.execute(plan)

    assert plan.is_complete()
    assert plan.progress() == 100.0


def test_execute_completed_plan():
    executor = PlanExecutor()

    plan = Plan(goal="Test")

    plan.add_step(
        create_step(
            1,
            "Done",
            PlanStatus.COMPLETED,
        )
    )

    executor.execute(plan)

    assert plan.is_complete()


def test_execute_step():
    executor = PlanExecutor()

    step = create_step(
        1,
        "Step",
    )

    executor.execute_step(step)

    assert step.status == PlanStatus.COMPLETED


def test_tool_router_called():
    """
    Executor should forward the step title
    to ToolRouter.
    """

    router = DummyToolRouter()

    executor = PlanExecutor(
        tool_router=router,
    )

    step = create_step(
        1,
        "Create folder demo",
    )

    executor.execute_step(step)

    assert router.calls == [
        "Create folder demo"
    ]

    assert (
        step.status
        == PlanStatus.COMPLETED
    )


def test_tool_router_execute_plan():
    """
    Every step should be routed.
    """

    router = DummyToolRouter()

    executor = PlanExecutor(
        tool_router=router,
    )

    plan = Plan(goal="Demo")

    plan.add_step(
        create_step(
            1,
            "Step One",
        )
    )

    plan.add_step(
        create_step(
            2,
            "Step Two",
        )
    )

    executor.execute(plan)

    assert router.calls == [
        "Step One",
        "Step Two",
    ]

    assert plan.is_complete()


from ai.execution_result import ExecutionResult


def test_execute_with_result_single_step():
    executor = PlanExecutor()

    plan = Plan(goal="Demo")

    plan.add_step(
        create_step(
            1,
            "Step One",
        )
    )

    result = executor.execute_with_result(plan)

    assert isinstance(result, ExecutionResult)
    assert result.success is True
    assert result.executed_steps == 1
    assert result.failed_steps == 0
    assert result.total_steps == 1
    assert result.has_failures is False
    assert result.outputs == [
        "Executed: Step One",
    ]
    assert plan.is_complete()


def test_execute_with_result_multiple_steps():
    executor = PlanExecutor()

    plan = Plan(goal="Demo")

    plan.add_step(
        create_step(
            1,
            "One",
        )
    )

    plan.add_step(
        create_step(
            2,
            "Two",
        )
    )

    result = executor.execute_with_result(plan)

    assert result.success is True
    assert result.executed_steps == 2
    assert result.failed_steps == 0
    assert result.total_steps == 2
    assert result.outputs == [
        "Executed: One",
        "Executed: Two",
    ]
    assert plan.is_complete()


def test_execute_with_result_empty_plan():
    executor = PlanExecutor()

    plan = Plan(goal="Empty")

    result = executor.execute_with_result(plan)

    assert result.success is True
    assert result.executed_steps == 0
    assert result.failed_steps == 0
    assert result.total_steps == 0
    assert result.outputs == []
    assert not plan.has_steps()
