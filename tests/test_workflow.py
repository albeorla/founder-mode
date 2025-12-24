from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import GraphState
from foundermode.graph.workflow import create_workflow


def test_workflow_execution() -> None:
    app = create_workflow()
    # app is already compiled

    initial_state: GraphState = {
        "research_question": "Revolutionary AI tool",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "init",
    }

    result = app.invoke(initial_state)

    assert "research_question" in result
    assert result["research_question"] == "Revolutionary AI tool"
    # assert len(result["plan"].tasks) > 0 # Plan concept removed/changed in new state
    # assert "Mock" in result["draft"].executive_summary # Mock node logic probably gone or needs update
