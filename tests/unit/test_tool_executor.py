
"""
Unit tests for ToolExecutor.
"""

from ai.tool_executor import ToolExecutor
from ai.tool_manager import ToolManager
from tools import CalculatorTool


def test_executor_runs_tool():
    """
    Executor should run registered tools.
    """

    manager = ToolManager()

    manager.register(
        CalculatorTool()
    )

    executor = ToolExecutor(
        manager
    )

    result = executor.execute(
        "calculator",
        expression="15 + 10",
    )

    assert result == "25"


def test_executor_missing_tool():
    """
    Executor should handle missing tools.
    """

    manager = ToolManager()

    executor = ToolExecutor(
        manager
    )

    result = executor.execute(
        "unknown"
    )

    assert (
        result
        == "Tool 'unknown' not found."
    )


def test_executor_exception_handling():
    """
    Executor should catch tool errors.
    """

    manager = ToolManager()

    manager.register(
        CalculatorTool()
    )

    executor = ToolExecutor(
        manager
    )

    result = executor.execute(
        "calculator",
        expression="invalid +"
    )

    assert result == "Invalid calculation."
