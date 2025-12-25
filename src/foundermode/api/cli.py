import os

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
from foundermode.utils.logging import setup_logging

# Load environment variables from .env file
load_dotenv()

# Force LangSmith off to stop 403 noise during debugging
os.environ["LANGCHAIN_TRACING_V2"] = "false"

# Setup logging
setup_logging()

app = typer.Typer(help="FounderMode: The Autonomous Due Diligence Agent", no_args_is_help=True)
console = Console()


@app.command(name="version")  # type: ignore
def version() -> None:
    """Print the version of FounderMode."""
    console.print("FounderMode v0.1.0")


@app.command(name="run")  # type: ignore
def run_command(
    query: str = typer.Argument(..., help="The business idea or market to research"),
    auto: bool = typer.Option(False, "--auto", "-a", help="Run without user confirmation"),
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
    input_to_graph: GraphState | None = initial_state

    while True:
        with console.status("[bold green]Agent Thinking...") as _:
            # stream returns events, we'll log them to see progress
            for event in workflow.stream(input_to_graph, config=config, stream_mode="updates"):
                for node_name, output in event.items():
                    console.print(f"[dim]Node [bold]{node_name}[/bold] completed.[/dim]")
                    if "next_step" in output:
                        console.print(f"[dim]  Transition -> [blue]{output['next_step']}[/blue][/dim]")
                    if "research_facts" in output:
                        count = len(output["research_facts"])
                        console.print(f"[dim]  Facts found: {count}[/dim]")

        # Check current status
        snapshot = workflow.get_state(config)

        if not snapshot.next:
            # Graph execution finished
            console.print("\n[bold green]✓ Research Complete![/bold green]\n")
            result_state = snapshot.values
            break

        # If we are here, the graph is interrupted
        current_values = snapshot.values
        next_node = snapshot.next[0]

        console.print(f"\n[bold yellow]⏸  Interrupt: Before {next_node}[/bold yellow]")

        # Show current progress
        facts = current_values.get("research_facts", [])
        console.print(f"[dim]Current fact count: {len(facts)}[/dim]")

        # Show the plan/topic if researcher is next
        if next_node == "researcher":
            topic = current_values.get("research_topic")
            console.print(f"[bold blue]Next Research Topic:[/bold blue] {topic}")

        if auto:
            console.print("[dim]Auto-proceeding...[/dim]")
            choice = "y"
        else:
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
    from pathlib import Path

    output_dir = Path(".out")
    output_dir.mkdir(exist_ok=True)

    filename = output_dir / f"{query.lower().replace(' ', '_')}_memo.html"
    render_memo(memo, str(filename))
    console.print(f"\n[dim]Report saved to {filename}[/dim]")


if __name__ == "__main__":
    app()
