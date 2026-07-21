
"""
Tool Router.

Connects tool detection,
argument extraction,
and execution.
"""

from __future__ import annotations

from ai.tool_argument_extractor import (
    ToolArgumentExtractor,
)
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
        argument_extractor: ToolArgumentExtractor | None = None,
    ) -> None:
        """
        Initialize tool router.
        """

        self._detector = detector

        self._executor = executor

        self._argument_extractor = (
            argument_extractor
            if argument_extractor is not None
            else ToolArgumentExtractor()
        )

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

        arguments = (
            self._argument_extractor.extract(
                tool_name,
                text,
            )
        )

        return self._executor.execute(
            tool_name,
            **arguments,
        )
