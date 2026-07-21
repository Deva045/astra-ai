"""
Unit tests for AI responses.
"""

from ai.response import (
    AIResponse,
    ResponseStatus,
)


def test_success_response():

    response = AIResponse(
        content="Hello Astra"
    )

    assert response.is_success
    assert (
        response.status
        == ResponseStatus.SUCCESS
    )


def test_error_response():

    response = AIResponse.error(
        "Something failed"
    )

    assert not response.is_success
    assert (
        response.status
        == ResponseStatus.ERROR
    )


def test_response_metadata():

    response = AIResponse(
        content="Hello",
        provider="ollama",
        model="qwen3",
    )

    assert response.provider == "ollama"
    assert response.model == "qwen3"
