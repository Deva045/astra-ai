"""
Unit tests for OllamaLLM.
"""

from __future__ import annotations

from unittest.mock import Mock, patch

import requests

from ai.ollama_llm import (
    OllamaConnectionError,
    OllamaLLM,
    OllamaResponseError,
)


def test_model_configuration():
    """
    OllamaLLM should store model configuration.
    """

    llm = OllamaLLM(
        model="qwen3"
    )

    assert llm.model == "qwen3"


def test_host_configuration():
    """
    OllamaLLM should store host configuration.
    """

    llm = OllamaLLM(
        host="http://localhost:11434/"
    )

    assert (
        llm.host
        == "http://localhost:11434"
    )


@patch("ai.ollama_llm.requests.get")
def test_is_available(mock_get):
    """
    Ollama availability check.
    """

    response = Mock()
    response.status_code = 200

    mock_get.return_value = response

    llm = OllamaLLM()

    assert llm.is_available()


@patch("ai.ollama_llm.requests.get")
def test_is_not_available(mock_get):
    """
    Ollama unavailable should return False.
    """

    mock_get.side_effect = requests.RequestException()

    llm = OllamaLLM()

    assert not llm.is_available()


@patch("ai.ollama_llm.requests.post")
def test_generate_response(mock_post):
    """
    Generate should return Ollama response.
    """

    response = Mock()

    response.json.return_value = {
        "response": "Hello Astra"
    }

    response.raise_for_status.return_value = None

    mock_post.return_value = response

    llm = OllamaLLM()

    result = llm.generate(
        "Hello"
    )

    assert result == "Hello Astra"


@patch("ai.ollama_llm.requests.post")
def test_generate_invalid_response(mock_post):
    """
    Invalid response should raise error.
    """

    response = Mock()

    response.json.return_value = {}

    response.raise_for_status.return_value = None

    mock_post.return_value = response

    llm = OllamaLLM()

    try:
        llm.generate(
            "Hello"
        )

    except OllamaResponseError:
        assert True

    else:
        assert False


@patch("ai.ollama_llm.requests.post")
def test_stream_response(mock_post):
    """
    Streaming should yield chunks.
    """

    response = Mock()

    response.raise_for_status.return_value = None

    response.iter_lines.return_value = [
        b'{"response":"Hello "}',
        b'{"response":"Astra"}',
        b'{"done":true}',
    ]

    mock_post.return_value = response

    llm = OllamaLLM()

    output = list(
        llm.stream(
            "Hello"
        )
    )

    assert output == [
        "Hello ",
        "Astra",
    ]


@patch("ai.ollama_llm.requests.post")
def test_connection_error(mock_post):
    """
    Connection failure should raise OllamaConnectionError.
    """

    mock_post.side_effect = (
        requests.RequestException()
    )

    llm = OllamaLLM(
        retries=0
    )

    try:
        llm.generate(
            "Hello"
        )

    except OllamaConnectionError:
        assert True

    else:
        assert False
