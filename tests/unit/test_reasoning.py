"""
Unit tests for the ReasoningEngine.
"""

from __future__ import annotations

from ai.reasoning import ReasoningEngine, ReasoningType


class TestReasoningEngine:
    """
    Tests for the ReasoningEngine.
    """

    def setup_method(self) -> None:
        """
        Create a fresh ReasoningEngine before each test.
        """
        self.engine = ReasoningEngine()

    def test_empty_input(self) -> None:
        """
        Empty input should default to chat.
        """
        assert (
            self.engine.classify("")
            == ReasoningType.CHAT
        )

    def test_help_command(self) -> None:
        """
        Help should be classified as a command.
        """
        assert (
            self.engine.classify("help")
            == ReasoningType.COMMAND
        )

    def test_command_alias(self) -> None:
        """
        Command aliases should be recognized.
        """
        assert (
            self.engine.classify("calc 5+5")
            == ReasoningType.COMMAND
        )

    def test_planning_create(self) -> None:
        """
        Create requests should be classified as planning.
        """
        assert (
            self.engine.classify(
                "Create folder Demo"
            )
            == ReasoningType.PLANNING
        )

    def test_planning_build(self) -> None:
        """
        Build requests should be classified as planning.
        """
        assert (
            self.engine.classify(
                "Build a website"
            )
            == ReasoningType.PLANNING
        )

    def test_chat(self) -> None:
        """
        Normal conversation should be classified as chat.
        """
        assert (
            self.engine.classify(
                "What is artificial intelligence?"
            )
            == ReasoningType.CHAT
        )

    def test_whitespace(self) -> None:
        """
        Leading and trailing whitespace should be ignored.
        """
        assert (
            self.engine.classify(
                "   help   "
            )
            == ReasoningType.COMMAND
        )

    def test_mixed_case(self) -> None:
        """
        Classification should be case-insensitive.
        """
        assert (
            self.engine.classify(
                "HeLp"
            )
            == ReasoningType.COMMAND
        )

    def test_generate_request(self) -> None:
        """
        Generate requests should be planning.
        """
        assert (
            self.engine.classify(
                "Generate documentation"
            )
            == ReasoningType.PLANNING
        )

    def test_make_request(self) -> None:
        """
        Make requests should be planning.
        """
        assert (
            self.engine.classify(
                "Make a desktop application"
            )
            == ReasoningType.PLANNING
        )
