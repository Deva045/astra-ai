
"""
Unit tests for ToolLoader.
"""

from ai.tool_loader import ToolLoader
from ai.tool_manager import ToolManager


def test_default_tools_loaded():
    """
    Default tools should be registered.
    """

    manager = ToolManager()

    ToolLoader.load_default_tools(
        manager
    )

    assert (
        "calculator"
        in manager.available_tools()
    )


def test_loaded_calculator_execution():
    """
    Loaded calculator should execute.
    """

    manager = ToolManager()

    ToolLoader.load_default_tools(
        manager
    )

    result = manager.execute(
        "calculator",
        expression="50 / 5",
    )

    assert result == "10"
