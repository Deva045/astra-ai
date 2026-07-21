"""
Unit tests for ContextManager.
"""

from ai.context_manager import (
    ContextManager,
    ContextMessage,
)


def test_context_keeps_recent_messages():
    """
    Context should keep only recent messages.
    """

    manager = ContextManager(
        max_messages=2
    )

    messages = [
        ContextMessage(
            role="user",
            content="old message",
        ),
        ContextMessage(
            role="assistant",
            content="middle message",
        ),
        ContextMessage(
            role="user",
            content="latest message",
        ),
    ]

    context = manager.build_context(
        messages
    )

    assert len(context.messages) == 2

    assert (
        context.messages[0].content
        == "middle message"
    )

    assert (
        context.messages[1].content
        == "latest message"
    )


def test_context_adds_memories():
    """
    Context should include memories.
    """

    manager = ContextManager()

    context = manager.build_context(
        messages=[],
        memories=[
            "User likes Python",
            "User builds AI projects",
        ],
    )

    assert len(context.memories) == 2

    prompt = context.to_prompt()

    assert "User likes Python" in prompt
    assert "User builds AI projects" in prompt


def test_context_prompt_generation():
    """
    Context should convert messages into prompt.
    """

    manager = ContextManager()

    context = manager.build_context(
        [
            ContextMessage(
                role="user",
                content="Hello",
            ),
            ContextMessage(
                role="assistant",
                content="Hi there",
            ),
        ]
    )

    prompt = context.to_prompt()

    assert "User: Hello" in prompt
    assert "Assistant: Hi there" in prompt


def test_context_trimming():
    """
    Large contexts should be reduced.
    """

    manager = ContextManager(
        max_chars=50
    )

    messages = [
        ContextMessage(
            role="user",
            content="A" * 100,
        ),
        ContextMessage(
            role="assistant",
            content="short",
        ),
    ]

    context = manager.build_context(
        messages
    )

    assert len(context.messages) == 1

    assert (
        context.messages[0].content
        == "short"
    )


def test_clear_context():
    """
    Clear should return empty context.
    """

    manager = ContextManager()

    context = manager.clear()

    assert context.messages == []
    assert context.memories == []
