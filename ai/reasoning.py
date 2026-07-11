"""
Reasoning engine for Nexus AI.

Determines how a user request should be processed.
"""

from __future__ import annotations

from ai.reasoning_result import ReasoningResult
from ai.reasoning_type import ReasoningType


class ReasoningEngine:
    """
    Determines how a user request should be handled.
    """

    def classify(self, text: str) -> ReasoningResult:
        """
        Classify a user request.

        Args:
            text:
                Raw user input.

        Returns:
            A ReasoningResult describing how the request
            should be processed.
        """
        text = text.strip().lower()

        if not text:
            return ReasoningResult(
                reasoning=ReasoningType.CHAT,
                confidence=1.0,
            )

        command_words = {
            "help",
            "version",
            "ver",
            "about",
            "clear",
            "cls",
            "exit",
            "quit",
            "date",
            "today",
            "time",
            "clock",
            "echo",
            "repeat",
            "calculate",
            "calc",
            "math",
            "history",
            "hist",
        }

        first_word = text.split(maxsplit=1)[0]

        if first_word in command_words:
            return ReasoningResult(
                reasoning=ReasoningType.COMMAND,
                confidence=1.0,
            )

        planning_prefixes = (
            "create ",
            "build ",
            "generate ",
            "make ",
        )

        if text.startswith(planning_prefixes):
            return ReasoningResult(
                reasoning=ReasoningType.PLANNING,
                confidence=0.95,
            )

        return ReasoningResult(
            reasoning=ReasoningType.CHAT,
            confidence=0.80,
        )
