"""
Unit tests for the command parser.
"""

from __future__ import annotations

from ai.command_parser import CommandParser, ParsedCommand


class TestCommandParser:
    """
    Tests for CommandParser.
    """

    def setup_method(self) -> None:
        """
        Create a fresh parser before each test.
        """
        self.parser = CommandParser()

    def test_parse_single_command(self) -> None:
        """
        A single command should parse correctly.
        """
        result = self.parser.parse("help")

        assert result == ParsedCommand(
            name="help",
            arguments="",
        )

    def test_parse_command_with_arguments(self) -> None:
        """
        Commands with arguments should preserve the arguments.
        """
        result = self.parser.parse("echo Hello World")

        assert result == ParsedCommand(
            name="echo",
            arguments="Hello World",
        )

    def test_parse_trims_whitespace(self) -> None:
        """
        Leading and trailing whitespace should be ignored.
        """
        result = self.parser.parse("   version   ")

        assert result == ParsedCommand(
            name="version",
            arguments="",
        )

    def test_parse_converts_command_to_lowercase(self) -> None:
        """
        Command names should be case-insensitive.
        """
        result = self.parser.parse("HeLp")

        assert result == ParsedCommand(
            name="help",
            arguments="",
        )

    def test_parse_preserves_argument_case(self) -> None:
        """
        Arguments should preserve their original case.
        """
        result = self.parser.parse("echo Hello Astra AI")

        assert result == ParsedCommand(
            name="echo",
            arguments="Hello Astra AI",
        )

    def test_parse_empty_string_returns_none(self) -> None:
        """
        Empty input should return None.
        """
        assert self.parser.parse("") is None

    def test_parse_whitespace_returns_none(self) -> None:
        """
        Whitespace-only input should return None.
        """
        assert self.parser.parse("     ") is None
