
"""
Tests for Planner.
"""

from ai.planner import Planner


def test_empty_goal():
    planner = Planner()

    plan = planner.create_plan("")

    assert plan.goal == ""
    assert plan.step_count() == 0


def test_create_folder():
    planner = Planner()

    plan = planner.create_plan(
        "Create folder demo"
    )

    assert plan.step_count() == 1
    assert (
        plan.steps[0].title
        == "Create folder demo"
    )


def test_create_file():
    planner = Planner()

    plan = planner.create_plan(
        "Create file main.py"
    )

    assert plan.step_count() == 1
    assert (
        plan.steps[0].title
        == "Create file main.py"
    )


def test_python_project():
    planner = Planner()

    plan = planner.create_plan(
        "Create a Python project called Demo"
    )

    assert plan.step_count() == 4

    assert (
        plan.steps[0].title
        == 'Create project folder "Demo"'
    )

    assert (
        plan.steps[-1].title
        == "Verify project structure"
    )


def test_multiple_steps():
    planner = Planner()

    plan = planner.create_plan(
        "Create folder demo. Create file main.py"
    )

    assert plan.step_count() == 2

    assert (
        plan.steps[0].title
        == "Create folder demo"
    )

    assert (
        plan.steps[1].title
        == "Create file main.py"
    )


def test_generic_plan():
    planner = Planner()

    plan = planner.create_plan(
        "Tell me a joke"
    )

    assert plan.step_count() == 1

    assert (
        plan.steps[0].title
        == "Tell me a joke"
    )


from ai.execution_result import ExecutionResult
from ai.plan_executor import PlanExecutor


def test_plan_and_execute():
    """
    Planner should create and execute a plan.
    """

    planner = Planner()

    executor = PlanExecutor()

    result = planner.plan_and_execute(
        "Create folder Demo",
        executor,
    )

    assert isinstance(
        result,
        ExecutionResult,
    )

    assert result.success is True

    assert result.executed_steps == 1

    assert result.failed_steps == 0

    assert result.outputs == [
        "Executed: Create folder Demo",
    ]


def test_plan_and_execute_empty_goal():
    planner = Planner()

    executor = PlanExecutor()

    result = planner.plan_and_execute(
        "",
        executor,
    )

    assert isinstance(
        result,
        ExecutionResult,
    )

    assert result.executed_steps == 0

    assert result.success is True
