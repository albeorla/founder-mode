from typing import get_type_hints

from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import GraphState


def test_graph_state_keys() -> None:
    hints = get_type_hints(GraphState)
    assert "research_question" in hints
    assert "research_facts" in hints
    assert "memo_draft" in hints
    assert "messages" in hints
    assert "next_step" in hints


def test_graph_state_types() -> None:
    hints = get_type_hints(GraphState)
    assert hints["research_question"] is str
    assert hints["memo_draft"] is InvestmentMemo
