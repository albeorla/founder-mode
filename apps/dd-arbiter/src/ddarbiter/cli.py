"""Command-line interface for DD-Arbiter."""

import asyncio
from pathlib import Path

import typer

from ddarbiter import __version__
from ddarbiter.graph import build_graph

app = typer.Typer(
    name="ddarbiter",
    help="Adversarial multi-model research for investment due diligence",
)


@app.command()
def analyze(
    document: Path = typer.Argument(..., help="Path to CIM or management presentation (PDF)"),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output path for report"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
    """Analyze a CIM or investment document with adversarial multi-model research.

    Runs three AI models in parallel:
    - Bull agent: Builds the strongest investment case
    - Bear agent: Attacks assumptions and finds weaknesses
    - Arbiter: Synthesizes with uncertainty quantification

    Outputs a structured report with:
    - Thesis confidence score (0-100)
    - Consensus claims (all models agree)
    - Disputed claims (models disagree)
    - Key risks and deal-breakers
    - Suggested diligence questions
    """
    if not document.exists():
        typer.echo(f"Error: Document not found: {document}", err=True)
        raise typer.Exit(1)

    if verbose:
        typer.echo(f"DD-Arbiter v{__version__}")
        typer.echo(f"Analyzing: {document}")

    # Build and run the graph
    graph = build_graph()

    # TODO: Implement actual document parsing
    initial_state = {
        "query": f"Analyze investment opportunity from {document.name}",
        "document_content": "",  # Will be populated by parse node
        "model_responses": [],
        "clusters": [],
        "disagreements": [],
        "uncertainty": {},
        "final_answer": {},
    }

    # Run async graph
    result = asyncio.run(_run_analysis(graph, initial_state))

    # Output results
    if output:
        output.write_text(str(result))
        typer.echo(f"Report saved to: {output}")
    else:
        typer.echo("\n--- Analysis Report ---\n")
        typer.echo(result.get("final_answer", {}))


async def _run_analysis(graph, initial_state: dict) -> dict:
    """Run the analysis graph asynchronously."""
    result = await graph.ainvoke(initial_state)
    return result


@app.command()
def version() -> None:
    """Show version information."""
    typer.echo(f"DD-Arbiter v{__version__}")


@app.command()
def demo() -> None:
    """Run a demo analysis on a sample document."""
    typer.echo("Demo mode - analyzing sample CIM...")
    typer.echo("\nNote: This is a placeholder. Full implementation coming soon.")
    typer.echo("\nExpected output:")
    typer.echo("  - Thesis Confidence Score: 72/100")
    typer.echo("  - Consensus Claims: 5 identified")
    typer.echo("  - Disputed Claims: 3 identified")
    typer.echo("  - Key Risks: 4 identified")
    typer.echo("  - Diligence Questions: 8 generated")


if __name__ == "__main__":
    app()
