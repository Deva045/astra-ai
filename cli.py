from rich.console import Console

from ai.router import Router

console = Console()
router = Router()


def main():
    console.print("[bold green]Nexus AI CLI[/bold green]")
    console.print("Type 'exit' to quit.\n")

    while True:
        text = console.input("[bold cyan]You:[/bold cyan] ")

        response = router.execute(text)

        if response.message == "__EXIT__":
            console.print("\n[bold yellow]Goodbye! 👋[/bold yellow]")
            break

        console.print(
            f"[bold green]Nexus:[/bold green] {response.message}"
        )


if __name__ == "__main__":
    main()
