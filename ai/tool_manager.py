"""
Tool Manager.

Provides a clean interface between the AI system
and the available tools.
"""

from __future__ import annotations

from tools import (
    Tool,
    ToolRegistry,
)


class ToolManager:
    """
    Manages AI tools.
    """

    def __init__(
        self,
        registry: ToolRegistry | None = None,
    ) -> None:
        """
        Initialize tool manager.
        """

        self._registry = (
            registry
            if registry is not None
            else ToolRegistry()
        )

    @property
    def registry(self) -> ToolRegistry:
        """
        Return tool registry.
        """

        return self._registry

    def register(
        self,
        tool: Tool,
    ) -> None:
        """
        Register a tool.
        """

        self._registry.register(
            tool
        )

    def execute(
        self,
        name: str,
        **kwargs,
    ) -> str:
        """
        Execute a tool by name.
        """

        tool = self._registry.get(
            name
        )

        if tool is None:
            return (
                f"Tool '{name}' "
                "not found."
            )

        return tool.execute(
            **kwargs
        )

    def available_tools(self) -> list[str]:
        """
        Return available tool names.
        """

        return self._registry.list_tools()
