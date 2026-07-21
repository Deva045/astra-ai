
"""
AIEngine tool integration tests.
"""

from ai.engine import AIEngine
from ai.tool_detector import ToolDetector
from ai.tool_executor import ToolExecutor
from ai.tool_manager import ToolManager
from ai.tool_router import ToolRouter
from tools import CalculatorTool


def create_engine_with_tools() -> AIEngine:
    """
    Create AIEngine with tools enabled.
    """

    manager = ToolManager()

    manager.register(
        CalculatorTool()
    )

    executor = ToolExecutor(
        manager
    )

    router = ToolRouter(
        ToolDetector(),
        executor,
    )

    return AIEngine(
        tool_router=router
    )


def test_ai_engine_uses_calculator_tool():
    """
    AIEngine should execute calculator requests.
    """

    engine = create_engine_with_tools()

    result = engine.chat(
        "calculate 25 + 5"
    )

    assert result == "30"


def test_ai_engine_normal_chat_without_tool():
    """
    Normal messages should still use AI.
    """

    engine = create_engine_with_tools()

    result = engine.chat(
        "Hello"
    )

    assert result is not None
