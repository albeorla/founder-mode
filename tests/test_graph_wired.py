from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import FounderState
from foundermode.graph.workflow import create_workflow, should_continue


def test_router_logic() -> None:
    state_research: FounderState = {
        "research_question": "Q",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "research",
        "research_topic": "T",
    }
    assert should_continue(state_research) == "researcher"

    state_write: FounderState = {
        "research_question": "Q",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "write",
        "research_topic": None,
    }
    assert should_continue(state_write) == "writer"


def test_workflow_compiles() -> None:
    app = create_workflow()
    assert app is not None


# We can't easily test the full execution flow with the real nodes without mocking the LLMs inside them,
# or we assume integration tests will cover that.
# The nodes themselves are tested in isolation.
# The router logic is tested above.
# The graph structure is declarative.
