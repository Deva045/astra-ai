
"""
Tests for ExecutionResult.
"""

from ai.execution_result import ExecutionResult


def test_default_values():
    result = ExecutionResult()

    assert result.success is True
    assert result.executed_steps == 0
    assert result.failed_steps == 0
    assert result.outputs == []


def test_add_output():
    result = ExecutionResult()

    result.add_output("Hello")

    assert result.outputs == [
        "Hello",
    ]


def test_total_steps():
    result = ExecutionResult(
        executed_steps=5,
        failed_steps=2,
    )

    assert result.total_steps == 7


def test_has_failures_true():
    result = ExecutionResult(
        failed_steps=1,
    )

    assert result.has_failures is True


def test_has_failures_false():
    result = ExecutionResult(
        failed_steps=0,
    )

    assert result.has_failures is False


def test_multiple_outputs():
    result = ExecutionResult()

    result.add_output("One")
    result.add_output("Two")
    result.add_output("Three")

    assert result.outputs == [
        "One",
        "Two",
        "Three",
    ]
