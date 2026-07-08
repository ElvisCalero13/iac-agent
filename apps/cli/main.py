import typer
from rich.console import Console
from rich.table import Table

from apps.cli.bootstrap import bootstrap_app

app = typer.Typer()
console = Console()

app.add_typer(bootstrap_app, name="bootstrap")

@app.command()
def version():
    console.print("[bold green]iac-agent[/bold green] 0.1.0")



if __name__ == "__main__":
    app()
