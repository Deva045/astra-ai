from rich.console import Console
from rich.panel import Panel

from config.constants import APP_NAME, VERSION
from core.startup import Startup

console = Console()


def banner():

    console.print()

    console.print(
        Panel.fit(
            f"[bold cyan]{APP_NAME}[/bold cyan]\n"
            f"[green]Version {VERSION}[/green]",
            border_style="cyan",
        )
    )


def main():

    banner()

    startup = Startup()

    startup.run()


if __name__ == "__main__":

    main()