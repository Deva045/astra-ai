"""
Unit tests for the HistoryCommand.
"""

from __future__ import annotations

from ai.commands.history_command import HistoryCommand
from ai.history import History


class TestHistoryCommand:
    """
    Tests for the HistoryCommand.
    """

    def test_empty_history(self) -> None:
        """
        The command should report when the history is empty.
        """
        history = History()
        command = HistoryCommand(history)

        result = command.execute("")

        assert result == "Command history is empty."

    def test_single_history_entry(self) -> None:
        """
        A single command should be displayed correctly.
        """
        history = History()
        history.add("help")

        command = HistoryCommand(history)

        expected = (
            "Command History\n"
            "---------------\n"
            "\n"
            "1. help"
        )

        assert command.execute("") == expected

    def test_multiple_history_entries(self) -> None:
        """
        Multiple commands should be displayed in execution order.
        """
        history = History()

        history.add("help")
        history.add("version")
        history.add("date")

        command = HistoryCommand(history)

        expected = (
            "Command History\n"
            "---------------\n"
            "\n"
            "1. help\n"
            "2. version\n"
            "3. date"
        )

        assert command.execute("") == expected

    def test_history_preserves_order(self) -> None:
        """
        Commands should appear in the same order they were executed.
        """
        history = History()

        commands = [
            "time",
            "echo hello",
            "calculate 5 + 5",
            "history",
        ]

        for item in commands:
            history.add(item)

        command = HistoryCommand(history)

        result = command.execute("")

        for index, item in enumerate(commands, start=1):
            assert f"{index}. {item}" in result

    def test_execute_returns_string(self) -> None:
        """
        Execute should always return a string.
        """
        history = History()

        command = HistoryCommand(history)

        result = command.execute("")

        assert isinstance(result, str)

    def test_history_does_not_modify_storage(self) -> None:
        """
        Executing the history command must not change stored history.
        """
        history = History()

        history.add("help")
        history.add("version")

        original = history.all().copy()

        command = HistoryCommand(history)

        command.execute("")

        assert history.all() == original

    def test_history_ignores_arguments(self) -> None:
        """
        Extra arguments should not affect the output.
        """
        history = History()

        history.add("help")

        command = HistoryCommand(history)

        expected = (
            "Command History\n"
            "---------------\n"
            "\n"
            "1. help"
        )

        assert command.execute("anything here") == expected
