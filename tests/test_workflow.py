from unittest.mock import patch

from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import FounderState
from foundermode.graph.workflow import create_workflow


def test_workflow_structure() -> None:
    app = create_workflow()
    # Check that it's a CompiledGraph
    assert hasattr(app, "invoke")
    assert hasattr(app, "stream")


def test_workflow_execution() -> None:
    # Patch the nodes to control the flow and avoid infinite recursion/LLM calls
    with (
        patch("foundermode.graph.workflow.planner_node") as mock_planner,
        patch("foundermode.graph.workflow.researcher_node") as mock_researcher,
        patch("foundermode.graph.workflow.writer_node") as mock_writer,
        patch("foundermode.graph.workflow.critic_node") as mock_critic,
    ):
        # Scenario: Planner -> Research -> Planner -> Write -> Critic -> End

        # 1. Planner called first. Returns 'research'.
        # 2. Researcher called. Returns facts.
        # 3. Planner called second. Returns 'write'.
        # 4. Writer called. Returns draft.
        # 5. Critic called. Returns 'approve'.

        mock_planner.side_effect = [
            {"next_step": "research", "research_topic": "Test Topic"},  # First call
            {"next_step": "write", "research_topic": None},  # Second call
        ]

        mock_researcher.return_value = {
            "research_facts": [],  # Just dummy update
            "next_step": "planner",
        }

        mock_writer.return_value = {
            "memo_draft": InvestmentMemo(executive_summary="Mock Exec Summary"),
            "next_step": "finish",
        }

        mock_critic.return_value = {
            "next_step": "approve",
            "critique_history": ["Good job"],
        }

        app = create_workflow(interrupt_before=[])

        initial_state: FounderState = {
            "research_question": "Revolutionary AI tool",
            "research_facts": [],
            "memo_draft": InvestmentMemo(),
            "messages": [],
            "next_step": "init",
            "research_topic": None,
            "critique_history": [],
            "revision_count": 0,
        }

        result = app.invoke(initial_state)

        # Assertions
        assert result["research_question"] == "Revolutionary AI tool"
        assert result["memo_draft"].executive_summary == "Mock Exec Summary"
        assert mock_planner.call_count == 2
        assert mock_researcher.call_count == 1
        assert mock_writer.call_count == 1
        assert mock_critic.call_count == 1
