
"""
Tool Loader.

Loads default Astra AI tools.
"""

from __future__ import annotations

from ai.tool_manager import ToolManager
from tools import CalculatorTool


class ToolLoader:
    """
    Loads built-in tools.
    """

    @staticmethod
    def load_default_tools(
        manager: ToolManager,
    ) -> None:
        """
        Register default tools.
        """

        manager.register(
            CalculatorTool()
        )
