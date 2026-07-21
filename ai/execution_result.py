
"""
Execution result model.

Represents the outcome of executing a plan.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ExecutionResult:
    """
    Result returned by PlanExecutor.

    Attributes
    ----------
    success:
        Overall execution status.

    executed_steps:
        Number of successfully executed steps.

    failed_steps:
        Number of failed steps.

    outputs:
        Messages produced during execution.
    """

    success: bool = True

    executed_steps: int = 0

    failed_steps: int = 0

    outputs: list[str] = field(
        default_factory=list,
    )

    def add_output(
        self,
        message: str,
    ) -> None:
        """
        Store an execution message.
        """

        self.outputs.append(
            message
        )

    @property
    def total_steps(
        self,
    ) -> int:
        """
        Total processed steps.
        """

        return (
            self.executed_steps
            + self.failed_steps
        )

    @property
    def has_failures(
        self,
    ) -> bool:
        """
        True if any step failed.
        """

        return self.failed_steps > 0
