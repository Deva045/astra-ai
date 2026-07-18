"""
Unit tests for OllamaProvider.
"""

from __future__ import annotations

from unittest.mock import Mock, patch

from ai.providers import OllamaProvider


def test_provider_name():
    provider = OllamaProvider()

    assert provider.provider_name == "ollama"


def test_model_name():
    provider = OllamaProvider(model_name="llama3")

    assert provider.model_name == "llama3"


@patch("ai.providers.ollama_provider.requests.get")
def test_is_available(mock_get):
    response = Mock()
    response.status_code = 200

    mock_get.return_value = response

    provider = OllamaProvider()

    assert provider.is_available()


@patch("ai.providers.ollama_provider.requests.get")
def test_available_models(mock_get):
    response = Mock()

    response.json.return_value = {
        "models": [
            {"name": "llama3"},
            {"name": "mistral"},
        ]
    }

    response.raise_for_status.return_value = None

    mock_get.return_value = response

    provider = OllamaProvider()

    assert provider.available_models() == [
        "llama3",
        "mistral",
    ]


@patch("ai.providers.ollama_provider.requests.post")
def test_generate(mock_post):
    response = Mock()

    response.json.return_value = {
        "response": "Hello from Ollama"
    }

    response.raise_for_status.return_value = None

    mock_post.return_value = response

    provider = OllamaProvider()

    assert (
        provider.generate("hello")
        == "Hello from Ollama"
    )
