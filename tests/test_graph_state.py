from typing import get_type_hints

from foundermode.domain.schema import InvestmentMemo, ResearchPlan
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
    assert hints["query"] is str
    assert hints["plan"] is ResearchPlan
    assert hints["draft"] is InvestmentMemo
