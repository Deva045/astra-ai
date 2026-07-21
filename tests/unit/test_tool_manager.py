"""
Unit tests for ToolManager.
"""

from ai.tool_manager import ToolManager
from tools import CalculatorTool


def test_register_tool():
    """
    ToolManager should register tools.
    """

    manager = ToolManager()

    manager.register(
        CalculatorTool()
    )

    assert (
        "calculator"
        in manager.available_tools()
    )


def test_execute_tool():
    """
    ToolManager should execute tools.
    """

    manager = ToolManager()

    manager.register(
        CalculatorTool()
    )

    result = manager.execute(
        "calculator",
        expression="20 + 5",
    )

    assert result == "25"


def test_missing_tool():
    """
    Unknown tools should return error.
    """

    manager = ToolManager()

    result = manager.execute(
        "unknown"
    )

    assert (
        result
        == "Tool 'unknown' not found."
    )
