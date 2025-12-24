from foundermode.domain.schema import InvestmentMemo
from foundermode.graph.workflow import create_workflow


def test_graph_compilation_and_execution() -> None:
    app = create_workflow()

    # Check that we got a compiled graph
    assert app is not None

    # Run the graph with minimal state
    initial_state = {
        "research_question": "Test",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "init",
    }

    # Invoke
    final_state = app.invoke(initial_state)

    # In our skeleton, it goes Planner -> Researcher -> Writer
    # The last node 'writer' returns next_step="finish"
    assert final_state["next_step"] == "finish"
