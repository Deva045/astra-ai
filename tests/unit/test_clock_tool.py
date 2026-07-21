
"""
Unit tests for ClockTool.
"""

from tools import ClockTool


def test_clock_tool_returns_time():
    """
    Clock tool should return a time string.
    """

    tool = ClockTool()

    result = tool.execute()

    assert isinstance(
        result,
        str,
    )

    assert len(result) == 8


def test_clock_tool_format():
    """
    Clock output should follow HH:MM:SS.
    """

    tool = ClockTool()

    result = tool.execute()

    parts = result.split(":")

    assert len(parts) == 3

    assert all(
        part.isdigit()
        for part in parts
    )
