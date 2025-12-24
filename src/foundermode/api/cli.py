import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from foundermode.domain.schema import InvestmentMemo, ResearchPlan
from foundermode.domain.state import GraphState
from foundermode.graph.workflow import create_workflow

# Load environment variables from .env file
load_dotenv()

app = typer.Typer(help="FounderMode: The Autonomous Due Diligence Agent", no_args_is_help=True)
console = Console()


@app.command(name="version")
def version() -> None:
    """Print the version of FounderMode."""
    console.print("FounderMode v0.1.0")


@app.command(name="run")
def run_command(
    query: str = typer.Argument(..., help="The business idea or market to research"),
) -> None:
    """Run the research agent on a business idea."""
    console.print(
        Panel(f"[bold blue]FounderMode[/bold blue]\nResearching: [italic]{query}[/italic]"),
        style="blue",
    )

    workflow = create_workflow()
    research_app = workflow.compile()

    # Initialize state
    initial_state: GraphState = {
        "query": query,
        "plan": ResearchPlan(tasks=[]),
        "facts": [],
        "draft": InvestmentMemo(),
        "messages": [],
    }

    with console.status("[bold green]Working...") as _:
        result = research_app.invoke(initial_state)  # type: ignore[arg-type]

    console.print("\n[bold green]✓ Research Complete![/bold green]\n")

    memo: InvestmentMemo = result["draft"]

    console.print(
        Panel(
            f"[bold]Executive Summary:[/bold]\n{memo.executive_summary}\n\n"
            f"[bold]Market Analysis:[/bold]\n{memo.market_analysis}\n\n"
            f"[bold]Competitive Landscape:[/bold]\n{memo.competitive_landscape}",
            title="[bold green]Investment Memo[/bold green]",
            border_style="green",
        )
    )


if __name__ == "__main__":
    app()
