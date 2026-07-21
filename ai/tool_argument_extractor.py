
"""
Tool Argument Extractor.

Extracts arguments required by tools.
"""

from __future__ import annotations


class ToolArgumentExtractor:
    """
    Extracts tool arguments from user text.
    """

    def extract(
        self,
        tool_name: str,
        text: str,
    ) -> dict[str, str]:
        """
        Extract arguments for a tool.
        """

        if tool_name == "calculator":
            return {
                "expression": self._extract_math(
                    text
                )
            }

        return {}

    def _extract_math(
        self,
        text: str,
    ) -> str:
        """
        Extract mathematical expression.
        """

        result = text.lower()

        replacements = {
            "divided by": " / ",
            "divide by": " / ",
            "times": " * ",
            "multiplied by": " * ",
            "multiply": " * ",
            "plus": " + ",
            "minus": " - ",
            "what is": " ",
            "calculate": " ",
            "calculation": " ",
            "solve": " ",
        }

        for word, replacement in replacements.items():
            result = result.replace(
                word,
                replacement,
            )

        return " ".join(
            result.split()
        )
