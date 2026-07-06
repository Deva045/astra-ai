"""
Astra AI - Console Entry Point
"""

from rich.console import Console

from ai.router import Router

console = Console()


def main() -> None:
    """Start the Astra AI CLI."""

    router = Router()

    console.print("[bold green]🚀 Astra AI[/bold green]")
    console.print("[dim]Type 'exit' to quit.[/dim]\n")

    while True:
        text = console.input("[bold cyan]You:[/bold cyan] ")

        if text.lower().strip() == "exit":
            console.print("\n👋 Goodbye!")
            break

        response = router.execute(text)

        console.print(f"[bold green]Astra:[/bold green] {response.message}")


if __name__ == "__main__":
    main()
