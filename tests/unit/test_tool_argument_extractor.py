
"""
Unit tests for ToolArgumentExtractor.
"""

from ai.tool_argument_extractor import ToolArgumentExtractor


def test_extract_calculator_expression():
    """
    Calculator expressions should be extracted.
    """

    extractor = ToolArgumentExtractor()

    result = extractor.extract(
        "calculator",
        "calculate 25 + 5",
    )

    assert (
        result["expression"]
        == "25 + 5"
    )


def test_extract_division_expression():
    """
    Division text should convert.
    """

    extractor = ToolArgumentExtractor()

    result = extractor.extract(
        "calculator",
        "50 divided by 5",
    )

    assert (
        result["expression"]
        == "50 / 5"
    )


def test_unknown_tool_returns_empty():
    """
    Unknown tools should return empty arguments.
    """

    extractor = ToolArgumentExtractor()

    result = extractor.extract(
        "unknown",
        "hello",
    )

    assert result == {}
