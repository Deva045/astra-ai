"""
Plan formatter for Nexus AI.

Converts execution plans into human-readable text.
"""

from __future__ import annotations

from ai.plan import Plan


class PlanFormatter:
    """
    Formats execution plans for display.
    """

    @staticmethod
    def format(plan: Plan) -> str:
        """
        Convert a plan into a human-readable string.

        Args:
            plan:
                The execution plan.

        Returns:
            Formatted plan text.
        """
        lines: list[str] = [
            f"Goal: {plan.goal}",
            "",
            "Steps",
            "-----",
        ]

        if not plan.steps:
            lines.append("No steps available.")
            return "\n".join(lines)

        for step in plan.steps:
            lines.append(f"{step.id}. {step.title}")

            if step.description:
                lines.append(f"   {step.description}")

        return "\n".join(lines)
