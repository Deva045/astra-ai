
"""
Tool confidence scoring.

Sprint 6.1

Provides confidence scores for built-in Astra AI tools while
remaining compatible with the existing ToolDetector.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from config.tool_config import DEFAULT_TOOL_CONFIG


@dataclass(slots=True)
class ToolMatch:
    """
    Represents a confidence match.
    """

    tool: str
    confidence: float


class ToolConfidence:
    """
    Confidence scorer for tool names.
    """

    MATH_PATTERN = re.compile(
        r"\d+\s*[\+\-\*/]\s*\d+"
    )

    def __init__(self) -> None:

        self._threshold = (
            DEFAULT_TOOL_CONFIG.confidence_threshold
        )

        self._max_confidence = (
            DEFAULT_TOOL_CONFIG.max_confidence
        )

        self._keywords = {
            "calculator": [
                "calculate",
                "calculation",
                "solve",
                "multiply",
                "times",
                "divide",
                "plus",
                "minus",
                "add",
                "subtract",
                "+",
                "-",
                "*",
                "/",
            ],
            "clock": [
                "time",
                "clock",
                "current time",
                "what time",
            ],
            "date": [
                "date",
                "today",
                "current date",
                "today's date",
            ],
        }

    def score(
        self,
        text: str,
    ) -> list[ToolMatch]:
        """
        Score every supported tool.
        """

        lowered = text.lower()

        results: list[ToolMatch] = []

        for tool, keywords in self._keywords.items():

            score = 0.0

            if (
                tool == "calculator"
                and self._contains_math_expression(
                    lowered
                )
            ):
                score += 3.0

            for keyword in keywords:

                if keyword in lowered:
                    score += 1.0

            confidence = min(
                score / 5.0,
                self._max_confidence,
            )

            results.append(
                ToolMatch(
                    tool=tool,
                    confidence=confidence,
                )
            )

        results.sort(
            key=lambda item: item.confidence,
            reverse=True,
        )

        return results

    def best_match(
        self,
        text: str,
    ) -> str | None:
        """
        Return the highest-confidence tool.
        """

        matches = self.score(text)

        if not matches:
            return None

        best = matches[0]

        if best.confidence < self._threshold:
            return None

        return best.tool

    def _contains_math_expression(
        self,
        text: str,
    ) -> bool:
        """
        Detect simple mathematical expressions.
        """

        return bool(
            self.MATH_PATTERN.search(
                text
            )
        )
