
"""
Plan execution engine for Astra AI.

Responsible for executing plans one step at a time.
"""

from __future__ import annotations

from ai.plan import Plan
from ai.execution_result import ExecutionResult
from ai.plan_status import PlanStatus
from ai.plan_step import PlanStep
from ai.tool_router import ToolRouter


class PlanExecutor:
    """
    Executes Plan objects.
    """

    def __init__(
        self,
        tool_router: ToolRouter | None = None,
    ) -> None:
        """
        Initialize the executor.

        Parameters
        ----------
        tool_router:
            Optional ToolRouter used to execute
            actionable plan steps.
        """

        self._tool_router = tool_router

    def execute(
        self,
        plan: Plan,
    ) -> Plan:
        """
        Execute every pending step.

        Returns
        -------
        Plan
            Updated execution plan.
        """

        for step in plan.pending_steps():
            self.execute_step(step)

        return plan

    def execute_step(
        self,
        step: PlanStep,
    ) -> None:
        """
        Execute a single plan step.
        """

        if self._tool_router is not None:
            self._tool_router.route(
                step.title
            )

        step.status = PlanStatus.COMPLETED



    def execute_with_result(
        self,
        plan: Plan,
    ) -> ExecutionResult:
        """
        Execute a plan and return an ExecutionResult.
        """

        result = ExecutionResult()

        for step in plan.pending_steps():
            self.execute_step(step)
            result.executed_steps += 1
            result.add_output(
                f"Executed: {step.title}"
            )

        result.success = (
            result.failed_steps == 0
        )

        return result

    def can_execute(
        self,
        plan: Plan,
    ) -> bool:
        """
        Return True if the plan contains work.
        """

        return (
            plan.has_steps()
            and not plan.is_complete()
        )
