"""
Astra AI Router

Decides which module should handle the user's request.
"""

from __future__ import annotations

from ai.bootstrap import create_command_registry
from ai.command_parser import CommandParser
from ai.engine import AIEngine
from ai.history import History
from ai.intent import IntentEngine
from ai.response import Response


class Router:
    """Routes user requests to the appropriate module."""

    def __init__(self) -> None:
        self.intent = IntentEngine()
        self.engine = AIEngine()

        # Shared services
        self.history = History()

        # Command Framework
        self.command_parser = CommandParser()
        self.command_registry = create_command_registry(
            self.history
        )

    def execute(self, text: str) -> Response:
        """
        Process a user request and return a Response object.
        """

        parsed = self.command_parser.parse(text)

        if parsed:
            command = self.command_registry.get(parsed.name)

            if command is not None:
                # Don't record the history command itself.
                if command.name != "history":
                    self.history.add(text)

                return Response(
                    success=True,
                    message=command.execute(parsed.arguments),
                )

        detected = self.intent.detect(text)

        if detected.name == "open_app":
            return Response(True, "Opening application...")

        if detected.name == "weather":
            return Response(True, "Weather module selected.")

        if detected.name == "time":
            return Response(True, "Clock module selected.")

        # Record normal AI prompts
        if text.strip():
            self.history.add(text)

        return Response(
            success=True,
            message=self.engine.chat(text),
        )

    def stream(self, text: str):
        """
        Stream AI responses.

        This method will be used by the CLI and GUI
        when a provider supports streaming.
        """

        parsed = self.command_parser.parse(text)

        if parsed:
            command = self.command_registry.get(parsed.name)

            if command is not None:
                if command.name != "history":
                    self.history.add(text)

                yield command.execute(parsed.arguments)
                return

        detected = self.intent.detect(text)

        if detected.name == "open_app":
            yield "Opening application..."
            return

        if detected.name == "weather":
            yield "Weather module selected."
            return

        if detected.name == "time":
            yield "Clock module selected."
            return

        if text.strip():
            self.history.add(text)

        yield from self.engine.stream_chat(text)
