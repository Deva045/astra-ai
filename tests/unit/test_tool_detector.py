
"""
Unit tests for ToolDetector.
"""

from ai.tool_detector import ToolDetector


def test_detect_calculator_keyword():
    """
    Calculator requests should be detected.
    """

    detector = ToolDetector()

    result = detector.detect(
        "calculate 25 + 5"
    )

    assert result == "calculator"


def test_detect_math_symbols():
    """
    Math symbols should trigger calculator.
    """

    detector = ToolDetector()

    result = detector.detect(
        "10 * 10"
    )

    assert result == "calculator"


def test_detect_normal_chat():
    """
    Normal messages should not trigger tools.
    """

    detector = ToolDetector()

    result = detector.detect(
        "Tell me about artificial intelligence"
    )

    assert result is None
