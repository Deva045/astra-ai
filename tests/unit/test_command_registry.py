"""
Unit tests for the command registry.
"""

from __future__ import annotations

import pytest

from ai.command import Command
from ai.command_registry import CommandRegistry


class DummyCommand(Command):
    """
    Dummy command used for registry testing.
    """

    @property
    def name(self) -> str:
        return "dummy"

    @property
    def aliases(self) -> list[str]:
        return ["d", "test"]

    def execute(self, arguments: str) -> str:
        return arguments


class AnotherCommand(Command):
    """
    Another dummy command used for duplicate tests.
    """

    @property
    def name(self) -> str:
        return "another"

    @property
    def aliases(self) -> list[str]:
        return ["a"]

    def execute(self, arguments: str) -> str:
        return arguments


class DuplicateNameCommand(Command):
    """
    Uses the same primary command name.
    """

    @property
    def name(self) -> str:
        return "dummy"

    def execute(self, arguments: str) -> str:
        return arguments


class DuplicateAliasCommand(Command):
    """
    Uses an alias that already exists.
    """

    @property
    def name(self) -> str:
        return "unique"

    @property
    def aliases(self) -> list[str]:
        return ["d"]

    def execute(self, arguments: str) -> str:
        return arguments


class TestCommandRegistry:
    """
    Tests for CommandRegistry.
    """

    def setup_method(self) -> None:
        """
        Create a fresh registry before each test.
        """
        self.registry = CommandRegistry()

    def test_register_command(self) -> None:
        """
        Registering a command should make it retrievable.
        """
        command = DummyCommand()

        self.registry.register(command)

        assert self.registry.get("dummy") is command

    def test_register_aliases(self) -> None:
        """
        Aliases should point to the same command.
        """
        command = DummyCommand()

        self.registry.register(command)

        assert self.registry.get("d") is command
        assert self.registry.get("test") is command

    def test_exists_returns_true(self) -> None:
        """
        Exists should return True for commands and aliases.
        """
        command = DummyCommand()

        self.registry.register(command)

        assert self.registry.exists("dummy")
        assert self.registry.exists("d")
        assert self.registry.exists("test")

    def test_exists_returns_false(self) -> None:
        """
        Unknown commands should not exist.
        """
        assert not self.registry.exists("missing")

    def test_get_returns_none(self) -> None:
        """
        Unknown commands should return None.
        """
        assert self.registry.get("missing") is None

    def test_duplicate_command_name_raises(self) -> None:
        """
        Duplicate primary command names are not allowed.
        """
        self.registry.register(DummyCommand())

        with pytest.raises(ValueError):
            self.registry.register(DuplicateNameCommand())

    def test_duplicate_alias_raises(self) -> None:
        """
        Duplicate aliases are not allowed.
        """
        self.registry.register(DummyCommand())

        with pytest.raises(ValueError):
            self.registry.register(DuplicateAliasCommand())

    def test_list_commands_returns_sorted_primary_names(self) -> None:
        """
        Only primary command names should be listed in sorted order.
        """
        self.registry.register(DummyCommand())
        self.registry.register(AnotherCommand())

        assert self.registry.list_commands() == [
            "another",
            "dummy",
        ]
