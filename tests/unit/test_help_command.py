"""
Unit tests for the help command.
"""

from __future__ import annotations

from ai.command_registry import CommandRegistry
from ai.commands.help_command import HelpCommand
from ai.command import Command


class DummyCommand(Command):
    """
    Dummy command used for testing HelpCommand.
    """

    @property
    def name(self) -> str:
        return "dummy"

    @property
    def aliases(self) -> list[str]:
        return ["d"]

    @property
    def category(self) -> str:
        return "Testing"

    @property
    def description(self) -> str:
        return "Dummy command."

    @property
    def usage(self) -> str:
        return "dummy"

    @property
    def examples(self) -> list[str]:
        return [
            "dummy",
            "d",
        ]

    def execute(self, arguments: str) -> str:
        return arguments


class TestHelpCommand:
    """
    Tests for HelpCommand.
    """

    def setup_method(self) -> None:
        """
        Create a fresh registry and help command.
        """
        self.registry = CommandRegistry()
        self.help_command = HelpCommand(self.registry)

    def test_no_registered_commands(self) -> None:
        """
        Help should report when no commands are registered.
        """
        assert (
            self.help_command.execute("")
            == "No commands are currently registered."
        )

    def test_general_help_lists_registered_commands(self) -> None:
        """
        General help should include registered commands.
        """
        self.registry.register(DummyCommand())

        output = self.help_command.execute("")

        assert "Nexus AI Commands" in output
        assert "dummy" in output
        assert "Dummy command." in output
        assert "Testing" in output

    def test_help_for_specific_command(self) -> None:
        """
        Detailed help should include command metadata.
        """
        self.registry.register(DummyCommand())

        output = self.help_command.execute("dummy")

        assert "Command: dummy" in output
        assert "Dummy command." in output
        assert "Testing" in output
        assert "Aliases" in output
        assert "d" in output
        assert "Usage" in output
        assert "Examples" in output

    def test_help_works_with_alias(self) -> None:
        """
        Detailed help should work with aliases.
        """
        self.registry.register(DummyCommand())

        output = self.help_command.execute("d")

        assert "Command: dummy" in output

    def test_unknown_command(self) -> None:
        """
        Unknown commands should return an error message.
        """
        output = self.help_command.execute("missing")

        assert output == "Unknown command: missing"
