
"""
Unit tests for tool metadata.
"""

from ai.tool_manager import ToolManager
from tools import CalculatorTool


def test_tool_metadata_available():
    """
    Tool metadata should be available.
    """

    manager = ToolManager()

    manager.register(
        CalculatorTool()
    )

    metadata = manager.available_metadata()

    assert len(metadata) == 1

    calculator = metadata[0]

    assert calculator["name"] == "calculator"

    assert (
        calculator["category"]
        == "math"
    )

    assert (
        "calculate 5 + 5"
        in calculator["examples"]
    )


def test_tool_metadata_description():
    """
    Tool description should exist.
    """

    manager = ToolManager()

    manager.register(
        CalculatorTool()
    )

    metadata = manager.available_metadata()

    assert (
        metadata[0]["description"]
        ==
        "Performs basic arithmetic calculations."
    )
