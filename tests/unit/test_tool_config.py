
"""
Tests for tool configuration.
"""

from config.tool_config import (
    DEFAULT_TOOL_CONFIG,
    ToolConfig,
)


def test_default_config_instance():
    """
    Default configuration should exist.
    """

    assert isinstance(
        DEFAULT_TOOL_CONFIG,
        ToolConfig,
    )


def test_default_threshold():
    """
    Default threshold should be valid.
    """

    assert (
        DEFAULT_TOOL_CONFIG.confidence_threshold
        == 0.15
    )


def test_max_confidence():
    """
    Maximum confidence should be 1.0.
    """

    assert (
        DEFAULT_TOOL_CONFIG.max_confidence
        == 1.0
    )


def test_threshold_range():
    """
    Threshold must be between 0 and 1.
    """

    assert (
        0.0
        <= DEFAULT_TOOL_CONFIG.confidence_threshold
        <= 1.0
    )


def test_max_confidence_range():
    """
    Maximum confidence must be positive.
    """

    assert (
        DEFAULT_TOOL_CONFIG.max_confidence
        > 0
    )
