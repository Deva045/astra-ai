
"""
Full multi-tool integration tests.
"""

from ai.tool_detector import ToolDetector
from ai.tool_executor import ToolExecutor
from ai.tool_manager import ToolManager
from ai.tool_router import ToolRouter
from tools import (
    CalculatorTool,
    ClockTool,
    DateTool,
)


def create_router() -> ToolRouter:
    """
    Create fully configured router.
    """

    manager = ToolManager()

    manager.register(
        CalculatorTool()
    )

    manager.register(
        ClockTool()
    )

    manager.register(
        DateTool()
    )

    return ToolRouter(
        ToolDetector(),
        ToolExecutor(manager),
    )


def test_calculator_full_flow():
    """
    Calculator should work end-to-end.
    """

    router = create_router()

    result = router.route(
        "calculate 20 + 10"
    )

    assert result == "30"


def test_clock_full_flow():
    """
    Clock should work end-to-end.
    """

    router = create_router()

    result = router.route(
        "what time is it"
    )

    assert isinstance(
        result,
        str,
    )


def test_date_full_flow():
    """
    Date should work end-to-end.
    """

    router = create_router()

    result = router.route(
        "what is today's date"
    )

    assert isinstance(
        result,
        str,
    )


def test_normal_message_bypass():
    """
    Normal messages should bypass tools.
    """

    router = create_router()

    result = router.route(
        "Explain machine learning"
    )

    assert result is None
