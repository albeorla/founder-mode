import typer
from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import GraphState
from foundermode.graph.workflow import create_workflow
from foundermode.tools.reporter import render_memo

# Load environment variables from .env file
load_dotenv()

app = typer.Typer(help="FounderMode: The Autonomous Due Diligence Agent", no_args_is_help=True)
console = Console()


@app.command(name="version")  # type: ignore
def version() -> None:
    """Print the version of FounderMode."""
    console.print("FounderMode v0.1.0")


@app.command(name="run")  # type: ignore
def run_command(
    query: str = typer.Argument(..., help="The business idea or market to research"),
) -> None:
    """Run the research agent on a business idea."""
    console.print(
        Panel(f"[bold blue]FounderMode[/bold blue]\nResearching: [italic]{query}[/italic]"),
        style="blue",
    )

    # 1. Initialize Graph with Checkpointer
    memory = MemorySaver()
    workflow = create_workflow(checkpointer=memory)

    # Use a static thread_id for the CLI session
    config: RunnableConfig = {"configurable": {"thread_id": "cli_session_1"}}

    # Initialize state
    initial_state: GraphState = {
        "research_question": query,
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "init",
        "research_topic": None,
    }

    # 2. Run the graph (handling interruptions)

    # First pass: Run until interruption or completion
    # We pass 'None' as input for subsequent resumes if we aren't updating state
    input_to_graph: GraphState | None = initial_state

    while True:
        with console.status("[bold green]Working...") as _:
            # stream returns events, but we just want to run until it stops
            for _event in workflow.stream(input_to_graph, config=config):
                pass

        # Check current status
        snapshot = workflow.get_state(config)

        if not snapshot.next:
            # Graph execution finished
            console.print("\n[bold green]✓ Research Complete![/bold green]\n")
            result_state = snapshot.values
            break

        # If we are here, the graph is interrupted
        # In our specific workflow, it interrupts before 'researcher'
        # Let's show the plan from the state
        current_values = snapshot.values
        research_plan = current_values.get("research_plan", [])

        console.print("\n[bold yellow]! Research Plan Generated[/bold yellow]")
        for task in research_plan:
            console.print(f"- {task}")

        # Ask user for input
        choice = Prompt.ask("Proceed?", choices=["y", "n", "edit"], default="y")

        if choice == "y":
            input_to_graph = None  # Resume execution
        elif choice == "n":
            console.print("[red]Aborted by user.[/red]")
            return
        elif choice == "edit":
            console.print("[dim](Edit feature not fully implemented, resuming for now)[/dim]")
            input_to_graph = None

    # 3. Output Result
    memo: InvestmentMemo = result_state["memo_draft"]

    # Handle case where memo might be None if failed
    if not memo:
        console.print("[red]No memo generated.[/red]")
        return

    console.print(
        Panel(
            f"[bold]Executive Summary:[/bold]\n{memo.executive_summary}\n\n"
            f"[bold]Market Analysis:[/bold]\n{memo.market_analysis}\n\n"
            f"[bold]Competitive Landscape:[/bold]\n{memo.competitive_landscape}",
            title="[bold green]Investment Memo[/bold green]",
            border_style="green",
        )
    )

    # Generate HTML Report
    filename = f"{query.lower().replace(' ', '_')}_memo.html"
    render_memo(memo, filename)
    console.print(f"\n[dim]Report saved to {filename}[/dim]")


if __name__ == "__main__":
    app()
