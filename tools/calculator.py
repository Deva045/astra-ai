"""
Calculator tool for Astra AI.
"""

from __future__ import annotations

import ast
import operator

from tools.base import Tool


class CalculatorTool(Tool):
    """
    Safe arithmetic calculator.
    """

    name = "calculator"

    description = (
        "Performs basic arithmetic calculations."
    )

    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }

    def execute(
        self,
        expression: str,
    ) -> str:
        """
        Calculate an arithmetic expression.
        """

        try:
            tree = ast.parse(
                expression,
                mode="eval",
            )

            result = self._evaluate(
                tree.body
            )

            if isinstance(result, float) and result.is_integer():
                return str(int(result))

            return str(result)

        except Exception:
            return "Invalid calculation."

    def _evaluate(
        self,
        node,
    ):
        """
        Safely evaluate AST nodes.
        """

        if isinstance(
            node,
            ast.Constant,
        ):
            if isinstance(
                node.value,
                (int, float),
            ):
                return node.value

        if isinstance(
            node,
            ast.BinOp,
        ):
            operation = self._operators.get(
                type(node.op)
            )

            if operation is None:
                raise ValueError()

            return operation(
                self._evaluate(node.left),
                self._evaluate(node.right),
            )

        raise ValueError()
