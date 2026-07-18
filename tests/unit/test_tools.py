"""
Unit tests for Astra AI tools.
"""

from tools import (
    CalculatorTool,
    ToolRegistry,
)


def test_tool_registration():
    """
    Registry should store tools.
    """

    registry = ToolRegistry()

    tool = CalculatorTool()

    registry.register(tool)

    assert registry.has_tool(
        "calculator"
    )

    assert (
        registry.get("calculator")
        == tool
    )


def test_tool_listing():
    """
    Registry should list tools.
    """

    registry = ToolRegistry()

    registry.register(
        CalculatorTool()
    )

    assert (
        "calculator"
        in registry.list_tools()
    )


def test_calculator_addition():
    """
    Calculator should add numbers.
    """

    calculator = CalculatorTool()

    result = calculator.execute(
        "10 + 5"
    )

    assert result == "15"


def test_calculator_multiplication():
    """
    Calculator should multiply numbers.
    """

    calculator = CalculatorTool()

    result = calculator.execute(
        "6 * 7"
    )

    assert result == "42"


def test_invalid_calculation():
    """
    Invalid expressions should fail safely.
    """

    calculator = CalculatorTool()

    result = calculator.execute(
        "hello world"
    )

    assert (
        result
        == "Invalid calculation."
    )
