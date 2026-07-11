"""
Unit tests for the Router.
"""

from __future__ import annotations

from ai.router import Router


class TestRouter:
    """
    Tests for the Router.
    """

    def setup_method(self) -> None:
        """
        Create a fresh Router before each test.
        """
        self.router = Router()

    def test_help_command(self) -> None:
        """
        Help command should return a successful response.
        """
        response = self.router.execute("help")

        assert response.success is True
        assert isinstance(response.message, str)

    def test_version_command(self) -> None:
        """
        Version command should execute successfully.
        """
        response = self.router.execute("version")

        assert response.success is True

    def test_calculate_command(self) -> None:
        """
        Calculate command should execute successfully.
        """
        response = self.router.execute("calculate 5+5")

        assert response.success is True
        assert response.message == "10"

    def test_history_command(self) -> None:
        """
        History command should execute successfully.
        """
        self.router.execute("help")

        response = self.router.execute("history")

        assert response.success is True
        assert "Command History" in response.message

    def test_chat_request(self) -> None:
        """
        Normal chat should be handled by the AI engine.
        """
        response = self.router.execute(
            "Hello Nexus"
        )

        assert response.success is True
        assert isinstance(response.message, str)

    def test_planning_request(self) -> None:
        """
        Planning requests should currently be handled
        without raising an exception.
        """
        response = self.router.execute(
            "Create folder Demo"
        )

        assert response.success is True

    def test_stream_command(self) -> None:
        """
        Streaming a command should return output.
        """
        chunks = list(
            self.router.stream(
                "version"
            )
        )

        assert len(chunks) == 1

    def test_stream_chat(self) -> None:
        """
        Streaming chat should produce output.
        """
        chunks = list(
            self.router.stream(
                "Hello Nexus"
            )
        )

        assert len(chunks) > 0
