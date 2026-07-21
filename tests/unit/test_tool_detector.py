
"""
Unit tests for ToolDetector.
"""

from ai.tool_detector import ToolDetector


def test_detect_calculator():
    """
    Calculator requests should detect.
    """

    detector = ToolDetector()

    assert (
        detector.detect(
            "calculate 10 + 5"
        )
        == "calculator"
    )


def test_detect_clock():
    """
    Time requests should detect.
    """

    detector = ToolDetector()

    assert (
        detector.detect(
            "what time is it"
        )
        == "clock"
    )


def test_detect_date():
    """
    Date requests should detect.
    """

    detector = ToolDetector()

    assert (
        detector.detect(
            "what is today's date"
        )
        == "date"
    )


def test_detect_normal_text():
    """
    Normal text should not detect tools.
    """

    detector = ToolDetector()

    assert (
        detector.detect(
            "Explain artificial intelligence"
        )
        is None
    )
