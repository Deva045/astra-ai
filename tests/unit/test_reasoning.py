"""
Unit tests for the ReasoningEngine.
"""

from __future__ import annotations

from ai.reasoning import ReasoningEngine
from ai.reasoning_type import ReasoningType


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
        result = self.engine.classify("")

        assert result.reasoning == ReasoningType.CHAT
        assert result.confidence == 1.0

    def test_help_command(self) -> None:
        """
        Help should be classified as a command.
        """
        result = self.engine.classify("help")

        assert result.reasoning == ReasoningType.COMMAND
        assert result.confidence == 1.0

    def test_command_alias(self) -> None:
        """
        Command aliases should be recognized.
        """
        result = self.engine.classify("calc 5+5")

        assert result.reasoning == ReasoningType.COMMAND
        assert result.confidence == 1.0

    def test_planning_create(self) -> None:
        """
        Create requests should be classified as planning.
        """
        result = self.engine.classify(
            "Create folder Demo"
        )

        assert result.reasoning == ReasoningType.PLANNING
        assert result.confidence == 0.95

    def test_planning_build(self) -> None:
        """
        Build requests should be classified as planning.
        """
        result = self.engine.classify(
            "Build a website"
        )

        assert result.reasoning == ReasoningType.PLANNING
        assert result.confidence == 0.95

    def test_generate_request(self) -> None:
        """
        Generate requests should be planning.
        """
        result = self.engine.classify(
            "Generate documentation"
        )

        assert result.reasoning == ReasoningType.PLANNING
        assert result.confidence == 0.95

    def test_make_request(self) -> None:
        """
        Make requests should be planning.
        """
        result = self.engine.classify(
            "Make a desktop application"
        )

        assert result.reasoning == ReasoningType.PLANNING
        assert result.confidence == 0.95

    def test_chat(self) -> None:
        """
        Normal conversation should be classified as chat.
        """
        result = self.engine.classify(
            "What is artificial intelligence?"
        )

        assert result.reasoning == ReasoningType.CHAT
        assert result.confidence == 0.80

    def test_whitespace(self) -> None:
        """
        Leading and trailing whitespace should be ignored.
        """
        result = self.engine.classify(
            "   help   "
        )

        assert result.reasoning == ReasoningType.COMMAND
        assert result.confidence == 1.0

    def test_mixed_case(self) -> None:
        """
        Classification should be case-insensitive.
        """
        result = self.engine.classify(
            "HeLp"
        )

        assert result.reasoning == ReasoningType.COMMAND
        assert result.confidence == 1.0

    def test_chat_confidence(self) -> None:
        """
        Chat requests should return the default confidence.
        """
        result = self.engine.classify(
            "Tell me a joke."
        )

        assert result.reasoning == ReasoningType.CHAT
        assert result.confidence == 0.80

    def test_planning_confidence(self) -> None:
        """
        Planning requests should return planning confidence.
        """
        result = self.engine.classify(
            "Create Python project"
        )

        assert result.reasoning == ReasoningType.PLANNING
        assert result.confidence == 0.95

    def test_command_confidence(self) -> None:
        """
        Commands should return maximum confidence.
        """
        result = self.engine.classify("history")

        assert result.reasoning == ReasoningType.COMMAND
        assert result.confidence == 1.0
