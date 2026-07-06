"""
Calculate command for Nexus AI.
"""

from __future__ import annotations

import ast
import operator

from ai.command import Command


_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
}


class CalculateCommand(Command):
    """
    Safely evaluate arithmetic expressions.
    """

    @property
    def name(self) -> str:
        return "calculate"

    @property
    def aliases(self) -> list[str]:
        return ["calc", "math"]

    @property
    def category(self) -> str:
        return "Utilities"

    @property
    def description(self) -> str:
        return "Evaluate an arithmetic expression."

    @property
    def usage(self) -> str:
        return "calculate <expression>"

    @property
    def examples(self) -> list[str]:
        return [
            "calculate 5 + 7",
            "calc 25 * 4",
            "math (10 + 5) / 3",
        ]

    def execute(self, arguments: str) -> str:
        if not arguments.strip():
            return "Usage: calculate <expression>"

        try:
            result = self._evaluate(ast.parse(arguments, mode="eval").body)
            return str(result)
        except Exception:
            return "Invalid mathematical expression."

    def _evaluate(self, node):
        if isinstance(node, ast.Constant):
            return node.value

        if isinstance(node, ast.BinOp):
            return _OPERATORS[type(node.op)](
                self._evaluate(node.left),
                self._evaluate(node.right),
            )

        if isinstance(node, ast.UnaryOp):
            return _OPERATORS[type(node.op)](
                self._evaluate(node.operand)
            )

        raise ValueError("Unsupported expression.")
