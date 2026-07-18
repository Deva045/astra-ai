"""
Tool registry for Astra AI.

Manages available tools and provides
tool lookup functionality.
"""

from __future__ import annotations

from tools.base import Tool


class ToolRegistry:
    """
    Stores and manages AI tools.
    """

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(
        self,
        tool: Tool,
    ) -> None:
        """
        Register a tool.
        """

        self._tools[tool.name] = tool

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove a tool.
        """

        self._tools.pop(
            name,
            None,
        )

    def get(
        self,
        name: str,
    ) -> Tool | None:
        """
        Retrieve a tool by name.
        """

        return self._tools.get(
            name
        )

    def list_tools(self) -> list[str]:
        """
        Return available tool names.
        """

        return list(
            self._tools.keys()
        )

    def has_tool(
        self,
        name: str,
    ) -> bool:
        """
        Check whether a tool exists.
        """

        return name in self._tools
