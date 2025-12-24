from unittest.mock import MagicMock, patch

from foundermode.api.cli import app
from typer.testing import CliRunner

runner = CliRunner()


@patch("foundermode.api.cli.create_workflow")
@patch("foundermode.api.cli.MemorySaver")
def test_cli_interactive_flow(mock_memory: MagicMock, mock_create_workflow: MagicMock) -> None:
    """
    Test that the CLI handles the graph interruption:
    1. Runs until 'interrupt_before'.
    2. Prompts user (simulated).
    3. Resumes execution.
    """
    # Setup Mock Graph
    mock_graph = MagicMock()
    mock_create_workflow.return_value = mock_graph

    # Mocking the state returned by get_state to simulate interruption
    # First call: Pause before Researcher
    state_at_pause = MagicMock()
    state_at_pause.next = ("researcher",)
    state_at_pause.values = {"research_plan": ["Find competitors"], "next_step": "research"}

    # Second call (after resume): Completed
    state_completed = MagicMock()
    state_completed.next = ()  # Empty tuple means finished
    # Return a mocked memo in the final result
    mock_memo = MagicMock()
    mock_memo.executive_summary = "Great idea"
    # Ensure memo_draft is available in values for the CLI extraction logic
    state_completed.values = {"memo_draft": mock_memo}

    # Configure get_state to return pause state first, then completed state
    mock_graph.get_state.side_effect = [state_at_pause, state_completed]

    # Mock stream to just yield nothing (we drive via get_state logic in this test)
    mock_graph.stream.return_value = []

    # Mock update_state for editing the plan
    mock_graph.update_state.return_value = None

    # Run CLI with inputs:
    # 1. "y" to approve the plan (or "n" to edit)
    # Let's test the "Approve" path first
    result = runner.invoke(app, ["run", "My Idea"], input="y\n")

    # Assertions
    if result.exit_code != 0:
        print(result.stdout)  # For debugging failures

    assert result.exit_code == 0
    assert "Research Plan Generated" in result.stdout
    assert "Find competitors" in result.stdout
    assert "Proceed?" in result.stdout

    # Verify we called stream twice: once to start, once to resume
    assert mock_graph.stream.call_count == 2
    # First call: initial state
    # Second call: Command.RESUME or None to continue

    # Also verify we initialized with a checkpointer
    mock_create_workflow.assert_called_with(checkpointer=mock_memory.return_value)
