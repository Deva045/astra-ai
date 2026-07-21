
"""
Clock tool for Astra AI.
"""

from __future__ import annotations

from datetime import datetime

from tools.base import Tool


class ClockTool(Tool):
    """
    Returns current system time.
    """

    name = "clock"

    description = (
        "Returns the current time."
    )

    category = "utility"

    examples = [
        "what time is it",
        "tell me the current time",
        "current time",
    ]

    def execute(
        self,
        **kwargs,
    ) -> str:
        """
        Return current time.
        """

        return datetime.now().strftime(
            "%H:%M:%S"
        )
