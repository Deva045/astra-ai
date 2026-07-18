
"""
Tool Detector.

Detects whether user input requires
a tool execution.
"""

from __future__ import annotations


class ToolDetector:
    """
    Rule-based tool detector.

    Uses simple intent matching now.
    Future versions can use AI-based
    tool selection.
    """

    def __init__(
        self,
        tool_metadata: list[dict] | None = None,
    ) -> None:
        """
        Initialize detector.

        Args:
            tool_metadata:
                Optional tool information.
        """

        self.tool_metadata = (
            tool_metadata
            if tool_metadata is not None
            else []
        )

    def detect(
        self,
        text: str,
    ) -> str | None:
        """
        Detect required tool.

        Returns:
            Tool name or None.
        """

        lowered = text.lower()

        math_keywords = [
            "calculate",
            "calculation",
            "solve",
            "multiply",
            "times",
            "divide",
            "divided",
            "plus",
            "add",
            "sum",
            "minus",
            "subtract",
            "difference",
            "product",
            "+",
            "-",
            "*",
            "/",
        ]

        if any(
            keyword in lowered
            for keyword in math_keywords
        ):
            return "calculator"

        if self._contains_math_expression(
            lowered
        ):
            return "calculator"

        return None

    def _contains_math_expression(
        self,
        text: str,
    ) -> bool:
        """
        Detect simple math expressions.
        """

        operators = [
            "+",
            "-",
            "*",
            "/",
        ]

        has_operator = any(
            operator in text
            for operator in operators
        )

        has_number = any(
            char.isdigit()
            for char in text
        )

        return (
            has_operator
            and has_number
        )
