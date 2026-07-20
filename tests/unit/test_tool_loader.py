
"""
Unit tests for ToolLoader.
"""

from ai.tool_loader import ToolLoader
from ai.tool_manager import ToolManager


def test_default_tools_loaded():
    """
    Default tools should load.
    """

    manager = ToolManager()

    ToolLoader.load_default_tools(
        manager
    )

    tools = manager.available_tools()

    assert "calculator" in tools

    assert "clock" in tools

    assert "date" in tools


def test_date_loaded_execution():
    """
    Date tool should execute.
    """

    manager = ToolManager()

    ToolLoader.load_default_tools(
        manager
    )

    result = manager.execute(
        "date"
    )

    assert isinstance(
        result,
        str,
    )
