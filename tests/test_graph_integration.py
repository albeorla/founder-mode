from unittest.mock import MagicMock, patch

import pytest

from foundermode.domain.schema import InvestmentMemo, ResearchFact
from foundermode.domain.state import FounderState
from foundermode.graph.workflow import create_workflow


@pytest.mark.integration
@pytest.mark.slow
def test_full_graph_execution_mocked() -> None:
    # 1. Setup Mock Nodes to simulate a full cycle:
    # planner -> researcher -> planner -> writer -> END

    # First call: research
    # Second call: write
    mock_planner = MagicMock()
    mock_planner.side_effect = [
        {"next_step": "research", "research_topic": "Topic A"},
        {"next_step": "write", "research_topic": None},
    ]

    mock_researcher = MagicMock()
    mock_researcher.return_value = {
        "research_facts": [ResearchFact(content="Fact A", source="S1")],
        "next_step": "planner",
    }

    mock_writer = MagicMock()
    mock_writer.return_value = {"memo_draft": InvestmentMemo(executive_summary="Mock Memo"), "next_step": "finish"}

    mock_critic = MagicMock()
    mock_critic.return_value = {"next_step": "approve", "critique_history": ["Good"]}

    with patch("foundermode.graph.workflow.planner_node", mock_planner):
        with patch("foundermode.graph.workflow.researcher_node", mock_researcher):
            with patch("foundermode.graph.workflow.writer_node", mock_writer):
                with patch("foundermode.graph.workflow.critic_node", mock_critic):
                    # Compile without HITL for easier testing
                    app = create_workflow(interrupt_before=[])

                    initial_state: FounderState = {
                        "research_question": "Test Question",
                        "research_facts": [],
                        "memo_draft": InvestmentMemo(),
                        "messages": [],
                        "next_step": "init",
                        "research_topic": None,
                        "search_history": [],
                        "critique_history": [],
                        "revision_count": 0,
                    }

                    # Execute
                    final_state = app.invoke(initial_state)

                # Verify Flow
                assert mock_planner.call_count == 2
                assert mock_researcher.call_count == 1
                assert mock_writer.call_count == 1

                assert final_state["memo_draft"].executive_summary == "Mock Memo"
                assert len(final_state["research_facts"]) == 1
