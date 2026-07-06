"""
Help command for Nexus AI.
"""

from __future__ import annotations

from collections import defaultdict

from ai.command import Command
from ai.command_registry import CommandRegistry


class HelpCommand(Command):
    """
    Displays all registered commands.
    """

    def __init__(self, registry: CommandRegistry) -> None:
        self._registry = registry

    @property
    def name(self) -> str:
        return "help"

    @property
    def aliases(self) -> list[str]:
        return ["h"]

    @property
    def category(self) -> str:
        return "Information"

    @property
    def description(self) -> str:
        return "Show all available commands."

    @property
    def usage(self) -> str:
        return "help [command]"

    @property
    def examples(self) -> list[str]:
        return [
            "help",
            "help version",
            "help calculate",
            "h",
        ]

    def execute(self, arguments: str) -> str:
        """
        Display general help or detailed help for a command.
        """
        arguments = arguments.strip()

        # Show detailed help for a specific command
        if arguments:
            command = self._registry.get(arguments)

            if command is None:
                return f"Unknown command: {arguments}"

            lines = [
                "=" * 40,
                f"Command: {command.name}",
                "=" * 40,
                "",
                "Description",
                "-----------",
                command.description,
                "",
                "Category",
                "--------",
                command.category,
            ]

            if command.aliases:
                lines.extend([
                    "",
                    "Aliases",
                    "-------",
                    ", ".join(command.aliases),
                ])

            lines.extend([
                "",
                "Usage",
                "-----",
                command.usage,
            ])

            if command.examples:
                lines.extend([
                    "",
                    "Examples",
                    "--------",
                ])

                for example in command.examples:
                    lines.append(example)

            return "\n".join(lines)

        # Show all commands grouped by category
        commands = []

        for command_name in self._registry.list_commands():
            command = self._registry.get(command_name)

            if command is not None:
                commands.append(command)

        if not commands:
            return "No commands are currently registered."

        grouped: dict[str, list[Command]] = defaultdict(list)

        for command in commands:
            grouped[command.category].append(command)

        lines = [
            "Nexus AI Commands",
            "=================",
            "",
        ]

        for category in sorted(grouped):
            lines.append(category)
            lines.append("-" * len(category))

            for command in sorted(grouped[category], key=lambda c: c.name):
                lines.append(
                    f"{command.name:<12} {command.description}"
                )

            lines.append("")

        lines.extend([
            "Tip:",
            "Type 'help <command>' for detailed information.",
        ])

        return "\n".join(lines).rstrip()
