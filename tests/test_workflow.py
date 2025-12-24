from foundermode.domain.schema import InvestmentMemo, ResearchPlan
from foundermode.domain.state import GraphState
from foundermode.graph.workflow import create_workflow


def test_workflow_execution() -> None:
    workflow = create_workflow()
    app = workflow.compile()

    initial_state: GraphState = {
        "query": "Revolutionary AI tool",
        "plan": ResearchPlan(tasks=[]),
        "facts": [],
        "draft": InvestmentMemo(),
        "messages": [],
    }

    result = app.invoke(initial_state)

    assert "query" in result
    assert result["query"] == "Revolutionary AI tool"
    assert len(result["plan"].tasks) > 0
    assert "Mock" in result["draft"].executive_summary
