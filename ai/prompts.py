"""
Prompt Builder.

Creates structured prompts for the LLM.
"""

from __future__ import annotations

from ai.personality import Personality


class PromptBuilder:
    """
    Builds optimized prompts for LLM providers.
    """

    PROMPT_VERSION = "1.1"

    @classmethod
    def build(
        cls,
        user_input: str,
        context: str = "",
    ) -> str:
        """
        Build a complete LLM prompt.

        Args:
            user_input:
                Current user message.

            context:
                Conversation and memory context.

        Returns:
            Formatted prompt.
        """

        sections: list[str] = []

        sections.append(
            "SYSTEM INSTRUCTIONS:\n"
            f"{Personality.system_prompt()}"
        )

        sections.append(
            "PROMPT METADATA:\n"
            f"Version: {cls.PROMPT_VERSION}"
        )

        if context.strip():
            sections.append(
                "CONTEXT:\n"
                f"{context.strip()}"
            )
        else:
            sections.append(
                "CONTEXT:\n"
                "No previous context available."
            )

        sections.append(
            "USER REQUEST:\n"
            f"{user_input.strip()}"
        )

        sections.append(
            "ASSISTANT RESPONSE:"
        )

        return "\n\n".join(
            sections
        )
