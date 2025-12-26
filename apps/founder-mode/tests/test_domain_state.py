from langchain_core.messages import HumanMessage

from foundermode.domain.schema import InvestmentMemo, ResearchFact
from foundermode.domain.state import FounderState


def test_founder_state_structure() -> None:
    # Verify that the keys exist and typing is correct (at runtime check)
    state: FounderState = {
        "research_question": "Test Question",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "init",
        "research_topic": None,
        "critique_history": [],
        "revision_count": 0,
    }

    assert state["research_question"] == "Test Question"
    assert isinstance(state["memo_draft"], InvestmentMemo)
    assert state["research_facts"] == []
    assert state["critique_history"] == []
    assert state["revision_count"] == 0


def test_founder_state_reducer() -> None:
    # Verify that annotated reducers work as expected (conceptually)
    # Since TypedDict doesn't enforce the reducer logic itself (LangGraph does),
    # we just check the annotation presence.

    annotations = FounderState.__annotations__
    assert "research_facts" in annotations
    assert "messages" in annotations
    assert "critique_history" in annotations

    # We can't easily test the 'operator.add' without the LangGraph runtime,
    # but we can verify the state object is valid python.

    fact1 = ResearchFact(content="A", source="S", relevance_score=1.0)
    fact2 = ResearchFact(content="B", source="S", relevance_score=1.0)

    state: FounderState = {
        "research_question": "Q",
        "research_facts": [fact1],
        "memo_draft": InvestmentMemo(),
        "messages": [HumanMessage(content="Hi")],
        "next_step": "research",
        "research_topic": None,
        "critique_history": ["Weak research"],
        "revision_count": 1,
    }

    # Simulate addition
    state["research_facts"] = state["research_facts"] + [fact2]
    assert len(state["research_facts"]) == 2

    state["critique_history"] = state["critique_history"] + ["Better but not there"]
    assert len(state["critique_history"]) == 2
