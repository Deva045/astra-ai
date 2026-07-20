
"""
Tool Detector.

Detects whether user input requires
a tool execution.
"""

from __future__ import annotations


class ToolDetector:
    """
    Rule-based tool detector.

    Uses intent matching.
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

    def detect(
        self,
        text: str,
    ) -> str | None:
        """
        Detect required tool.
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

        time_keywords = [
            "what time",
            "current time",
            "tell me the time",
            "time is it",
            "clock",
        ]

        if any(
            keyword in lowered
            for keyword in time_keywords
        ):
            return "clock"

        date_keywords = [
            "what date",
            "today's date",
            "todays date",
            "current date",
            "date today",
        ]

        if any(
            keyword in lowered
            for keyword in date_keywords
        ):
            return "date"

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
