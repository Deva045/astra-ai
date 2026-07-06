"""
Prompt Builder.
"""

from __future__ import annotations

from ai.personality import Personality


class PromptBuilder:
    """Builds prompts for the LLM."""

    PROMPT_VERSION = "1.0"

    @classmethod
    def build(
        cls,
        user_input: str,
        context: str = ""
    ) -> str:

        return (
            f"{Personality.system_prompt()}\n\n"
            f"Prompt Version: {cls.PROMPT_VERSION}\n\n"
            f"Conversation History:\n"
            f"{context}\n\n"
            f"Current User Message:\n"
            f"{user_input}\n\n"
            f"Assistant:"
        )
