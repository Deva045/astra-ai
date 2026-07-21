
"""
Plan parser for Astra AI.

Responsible for parsing user requests into
normalized planning instructions.
"""

from __future__ import annotations

import re


class PlanParser:
    """
    Parses user goals into normalized instructions.
    """

    def parse(
        self,
        goal: str,
    ) -> list[str]:
        """
        Parse a user goal into individual instructions.
        """

        goal = goal.strip()

        if not goal:
            return []

        instructions = [
            self.normalize(item)
            for item in re.split(
                r"\.\s+|\band then\b|\bthen\b",
                goal,
                flags=re.IGNORECASE,
            )
            if item.strip()
        ]

        return instructions

    def normalize(
        self,
        instruction: str,
    ) -> str:
        """
        Normalize whitespace and punctuation.
        """

        instruction = re.sub(
            r"\s+",
            " ",
            instruction.strip(),
        )

        return instruction.rstrip(".")

    def is_multi_step(
        self,
        goal: str,
    ) -> bool:
        """
        Return True if the request contains
        multiple instructions.
        """

        return len(self.parse(goal)) > 1
