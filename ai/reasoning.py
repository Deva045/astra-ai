"""
Reasoning engine for Astra AI.

Responsible for determining how a user request should be handled.
"""

from __future__ import annotations

from enum import Enum


class ReasoningType(str, Enum):
    """
    Represents the type of reasoning required
    for a user request.
    """

    COMMAND = "command"
    PLANNING = "planning"
    CHAT = "chat"
    AUTOMATION = "automation"
    MEMORY = "memory"


class ReasoningEngine:
    """
    Determines how Astra should process
    a user's request.
    """

    def classify(self, text: str) -> ReasoningType:
        """
        Classify a user request.

        Args:
            text:
                User input.

        Returns:
            The reasoning type.
        """
        text = text.strip().lower()

        if not text:
            return ReasoningType.CHAT

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
            return ReasoningType.COMMAND

        planning_prefixes = (
            "create ",
            "build ",
            "generate ",
            "make ",
        )

        if text.startswith(planning_prefixes):
            return ReasoningType.PLANNING

        return ReasoningType.CHAT
