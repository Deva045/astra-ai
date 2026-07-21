
"""
Tests for ToolConfidence.
"""

from ai.tool_confidence import ToolConfidence


def test_detect_calculator():
    confidence = ToolConfidence()

    assert (
        confidence.best_match(
            "calculate 20 + 10"
        )
        == "calculator"
    )


def test_detect_math_expression():
    confidence = ToolConfidence()

    assert (
        confidence.best_match(
            "25 * 8"
        )
        == "calculator"
    )


def test_detect_clock():
    confidence = ToolConfidence()

    assert (
        confidence.best_match(
            "what time is it"
        )
        == "clock"
    )


def test_detect_date():
    confidence = ToolConfidence()

    assert (
        confidence.best_match(
            "what is today's date"
        )
        == "date"
    )


def test_unknown_input():
    confidence = ToolConfidence()

    assert (
        confidence.best_match(
            "tell me about python programming"
        )
        is None
    )


def test_score_order():
    confidence = ToolConfidence()

    scores = confidence.score(
        "calculate 5 + 5"
    )

    assert scores[0].tool == "calculator"
    assert scores[0].confidence >= scores[1].confidence
