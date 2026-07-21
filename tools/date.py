
"""
Date tool for Astra AI.
"""

from __future__ import annotations

from datetime import datetime

from tools.base import Tool


class DateTool(Tool):
    """
    Returns current date.
    """

    name = "date"

    description = (
        "Returns the current date."
    )

    category = "utility"

    examples = [
        "what is today's date",
        "tell me the current date",
        "today's date",
    ]

    def execute(
        self,
        **kwargs,
    ) -> str:
        """
        Return current date.
        """

        return datetime.now().strftime(
            "%Y-%m-%d"
        )
