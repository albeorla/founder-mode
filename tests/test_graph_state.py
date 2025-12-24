from typing import List, get_type_hints
from langchain_core.messages import BaseMessage
from foundermode.domain.schema import ResearchPlan, ResearchFact, InvestmentMemo
from foundermode.domain.state import GraphState

def test_graph_state_keys() -> None:
    hints = get_type_hints(GraphState)
    assert "query" in hints
    assert "plan" in hints
    assert "facts" in hints
    assert "draft" in hints
    assert "messages" in hints

def test_graph_state_types() -> None:
    hints = get_type_hints(GraphState)
    assert hints["query"] == str
    assert hints["plan"] == ResearchPlan
    assert hints["draft"] == InvestmentMemo
