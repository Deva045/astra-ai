"""
Unit tests for AIManager.
"""

from ai import AIManager


def test_default_provider():
    manager = AIManager()

    assert manager.provider_name == "mock"


def test_generate():
    manager = AIManager()

    response = manager.generate("Hello")

    assert response == "Mock Response: Hello"


def test_switch_provider():
    manager = AIManager()

    manager.set_provider("mock")

    assert manager.provider_name == "mock"


def test_available_models():
    manager = AIManager()

    assert manager.available_models() == ["mock-model"]


def test_is_available():
    manager = AIManager()

    assert manager.is_available()
