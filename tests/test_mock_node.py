from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import GraphState
from foundermode.graph.nodes.mock import mock_analyst


def test_mock_analyst_updates_state() -> None:
    initial_state: GraphState = {
        "research_question": "Test idea",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "init",
    }

    result = mock_analyst(initial_state)

    # assert len(result["plan"].tasks) > 0 # Removed plan
    assert result["memo_draft"].executive_summary != ""
    assert "Mock" in result["memo_draft"].executive_summary
