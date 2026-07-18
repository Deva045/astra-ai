
"""
Tool Router.

Connects tool detection with execution.
"""

from __future__ import annotations

from ai.tool_detector import ToolDetector
from ai.tool_executor import ToolExecutor


class ToolRouter:
    """
    Routes user requests to tools.
    """

    def __init__(
        self,
        detector: ToolDetector,
        executor: ToolExecutor,
    ) -> None:
        """
        Initialize tool router.
        """

        self._detector = detector
        self._executor = executor

    def route(
        self,
        text: str,
    ) -> str | None:
        """
        Detect and execute a tool.

        Returns:
            Tool result or None.
        """

        tool_name = self._detector.detect(
            text
        )

        if tool_name is None:
            return None

        expression = self._extract_expression(
            text
        )

        return self._executor.execute(
            tool_name,
            expression=expression,
        )

    def _extract_expression(
        self,
        text: str,
    ) -> str:
        """
        Extract calculation expression.

        Simple implementation.
        Improved parsing comes later.
        """

        replacements = [
            "calculate",
            "solve",
            "multiply",
            "divide",
        ]

        result = text.lower()

        for word in replacements:
            result = result.replace(
                word,
                "",
            )

        return result.strip()
