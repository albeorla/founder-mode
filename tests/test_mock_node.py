from foundermode.domain.state import GraphState
from foundermode.domain.schema import ResearchPlan, InvestmentMemo
from foundermode.graph.nodes.mock import mock_analyst

def test_mock_analyst_updates_state() -> None:
    initial_state: GraphState = {
        "query": "Test idea",
        "plan": ResearchPlan(tasks=[]),
        "facts": [],
        "draft": InvestmentMemo(),
        "messages": []
    }
    
    result = mock_analyst(initial_state)
    
    assert len(result["plan"].tasks) > 0
    assert result["draft"].executive_summary != ""
    assert "Mock" in result["draft"].executive_summary
