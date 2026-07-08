"""
Unit tests for the CalculateCommand.
"""

from __future__ import annotations

from ai.commands.calculate_command import CalculateCommand


class TestCalculateCommand:
    """
    Tests for the CalculateCommand.
    """

    def setup_method(self) -> None:
        self.command = CalculateCommand()

    def test_addition(self) -> None:
        assert self.command.execute("5 + 7") == "12"

    def test_subtraction(self) -> None:
        assert self.command.execute("10 - 3") == "7"

    def test_multiplication(self) -> None:
        assert self.command.execute("6 * 4") == "24"

    def test_division(self) -> None:
        assert self.command.execute("20 / 5") == "4.0"

    def test_parentheses(self) -> None:
        assert self.command.execute("(2 + 3) * 4") == "20"

    def test_power(self) -> None:
        assert self.command.execute("2 ** 5") == "32"

    def test_modulo(self) -> None:
        assert self.command.execute("10 % 3") == "1"

    def test_floor_division(self) -> None:
        assert self.command.execute("7 // 2") == "3"

    def test_negative_number(self) -> None:
        assert self.command.execute("-5") == "-5"

    def test_float_expression(self) -> None:
        assert self.command.execute("2.5 + 3.5") == "6.0"

    def test_whitespace_is_ignored(self) -> None:
        assert self.command.execute("   8 + 2   ") == "10"

    def test_empty_expression(self) -> None:
        assert (
            self.command.execute("")
            == "Usage: calculate <expression>"
        )

    def test_whitespace_only_expression(self) -> None:
        assert (
            self.command.execute("     ")
            == "Usage: calculate <expression>"
        )

    def test_invalid_expression(self) -> None:
        assert (
            self.command.execute("2 +")
            == "Invalid mathematical expression."
        )

    def test_division_by_zero(self) -> None:
        assert (
            self.command.execute("5 / 0")
            == "Invalid mathematical expression."
        )

    def test_unsupported_expression(self) -> None:
        assert (
            self.command.execute("abs(5)")
            == "Invalid mathematical expression."
        )

    def test_execute_returns_string(self) -> None:
        result = self.command.execute("1 + 1")
        assert isinstance(result, str)
