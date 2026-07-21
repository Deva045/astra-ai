
"""
Unit tests for DateTool.
"""

from tools import DateTool


def test_date_tool_returns_date():
    """
    Date tool should return a date string.
    """

    tool = DateTool()

    result = tool.execute()

    assert isinstance(
        result,
        str,
    )

    assert len(result) == 10


def test_date_tool_format():
    """
    Date should follow YYYY-MM-DD.
    """

    tool = DateTool()

    result = tool.execute()

    parts = result.split("-")

    assert len(parts) == 3

    assert all(
        part.isdigit()
        for part in parts
    )
