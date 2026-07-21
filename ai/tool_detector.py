
"""
Tool Detector.

Detects whether user input requires
tool execution using confidence scoring.
"""

from __future__ import annotations

from ai.tool_confidence import ToolConfidence


class ToolDetector:
    """
    Detect the most appropriate tool
    using the confidence engine.
    """

    def __init__(
        self,
        tool_metadata: list[dict] | None = None,
    ) -> None:
        """
        Initialize detector.
        """

        self.tool_metadata = (
            tool_metadata
            if tool_metadata is not None
            else []
        )

        self._confidence = ToolConfidence()

    def detect(
        self,
        text: str,
    ) -> str | None:
        """
        Detect the best matching tool.

        Returns:
            Tool name or None.
        """

        return self._confidence.best_match(
            text
        )
