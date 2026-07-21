
"""
Tests for the plan parser.
"""

from ai.plan_parser import PlanParser


def test_empty_goal():
    """
    Empty goals should produce no instructions.
    """
    parser = PlanParser()

    assert parser.parse("") == []
    assert not parser.is_multi_step("")


def test_single_instruction():
    """
    Single instructions should remain unchanged.
    """
    parser = PlanParser()

    result = parser.parse(
        "Create folder demo"
    )

    assert result == [
        "Create folder demo"
    ]

    assert not parser.is_multi_step(
        "Create folder demo"
    )


def test_multiple_sentences():
    """
    Sentences separated by periods
    should become separate instructions.
    """
    parser = PlanParser()

    result = parser.parse(
        "Create folder demo. Create file main.py"
    )

    assert result == [
        "Create folder demo",
        "Create file main.py",
    ]

    assert parser.is_multi_step(
        "Create folder demo. Create file main.py"
    )


def test_then_separator():
    """
    'then' should split instructions.
    """
    parser = PlanParser()

    result = parser.parse(
        "Calculate 2+2 then tell me the date"
    )

    assert result == [
        "Calculate 2+2",
        "tell me the date",
    ]


def test_and_then_separator():
    """
    'and then' should split instructions.
    """
    parser = PlanParser()

    result = parser.parse(
        "Open calculator and then calculate 5*8"
    )

    assert result == [
        "Open calculator",
        "calculate 5*8",
    ]


def test_normalize():
    """
    Extra whitespace and periods
    should be removed.
    """
    parser = PlanParser()

    assert (
        parser.normalize(
            "   Create    folder   demo.   "
        )
        == "Create folder demo"
    )
