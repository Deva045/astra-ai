
"""
Tool Execution Service.

Provides safe execution of registered tools.
"""

from __future__ import annotations

from ai.tool_manager import ToolManager


class ToolExecutor:
    """
    Executes tools through ToolManager.
    """

    def __init__(
        self,
        tool_manager: ToolManager,
    ) -> None:
        """
        Initialize executor.
        """

        self._tool_manager = tool_manager

    @property
    def tool_manager(self) -> ToolManager:
        """
        Return the tool manager.
        """

        return self._tool_manager

    def execute(
        self,
        tool_name: str,
        **kwargs,
    ) -> str:
        """
        Execute a tool safely.
        """

        try:
            return self._tool_manager.execute(
                tool_name,
                **kwargs,
            )

        except Exception as exc:
            return (
                f"Tool execution failed: {exc}"
            )
