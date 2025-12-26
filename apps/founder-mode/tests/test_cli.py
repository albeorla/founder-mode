from unittest.mock import patch

from typer.testing import CliRunner

from foundermode.api.cli import app
from foundermode.domain.schema import InvestmentMemo

runner = CliRunner()


def test_cli_run_success() -> None:
    # Patch nodes to avoid LLM calls and recursion
    with (
        patch("foundermode.graph.workflow.planner_node") as mock_planner,
        patch("foundermode.graph.workflow.researcher_node") as _,
        patch("foundermode.graph.workflow.writer_node") as mock_writer,
    ):
        mock_planner.return_value = {"next_step": "write"}
        mock_writer.return_value = {
            "memo_draft": InvestmentMemo(
                executive_summary="Mock Executive Summary",
                market_analysis="Mock Market",
                competitive_landscape="Mock Competition",
            )
        }

        result = runner.invoke(app, ["run", "Test Idea"])
    assert result.exit_code == 0
    assert "FounderMode" in result.stdout
    assert "Researching: Test Idea" in result.stdout
    # Skeleton graph returns empty memo, so we check for the structure headers
    assert "Executive Summary:" in result.stdout
    assert "Market Analysis:" in result.stdout
