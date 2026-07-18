
"""
Unit tests for ToolRouter.
"""

from ai.tool_detector import ToolDetector
from ai.tool_executor import ToolExecutor
from ai.tool_manager import ToolManager
from ai.tool_router import ToolRouter
from tools import CalculatorTool


def create_router() -> ToolRouter:
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


def test_route_calculation():
    """
    Calculator requests should execute.
    """

    router = create_router()

    result = router.route(
        "calculate 25 + 5"
    )

    assert result == "30"


def test_route_math_symbol():
    """
    Math symbols should execute.
    """

    router = create_router()

    result = router.route(
        "10 * 5"
    )

    assert result == "50"


def test_route_normal_message():
    """
    Normal messages should not use tools.
    """

    router = create_router()

    result = router.route(
        "Explain machine learning"
    )

    assert result is None
