
"""
Tests for AIEngine tool integration.
"""

from ai.tool_detector import ToolDetector
from ai.tool_executor import ToolExecutor
from ai.tool_manager import ToolManager
from ai.tool_router import ToolRouter
from tools import CalculatorTool


def create_tool_router() -> ToolRouter:
    """
    Create configured tool router.
    """

    manager = ToolManager()

    manager.register(
        CalculatorTool()
    )

    executor = ToolExecutor(
        manager
    )

    detector = ToolDetector()

    return ToolRouter(
        detector,
        executor,
    )


def test_calculation_request_uses_tool():
    """
    Calculator requests should return tool result.
    """

    router = create_tool_router()

    result = router.route(
        "calculate 100 / 5"
    )

    assert result == "20"


def test_non_tool_request_returns_none():
    """
    Normal conversation should not trigger tools.
    """

    router = create_tool_router()

    result = router.route(
        "What is artificial intelligence?"
    )

    assert result is None
