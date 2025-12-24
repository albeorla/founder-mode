from typing import Any

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from foundermode.domain.state import FounderState


# Placeholder Nodes
def planner(state: FounderState) -> dict[str, Any]:
    return {"next_step": "research"}


def researcher(state: FounderState) -> dict[str, Any]:
    return {"next_step": "write"}


def writer(state: FounderState) -> dict[str, Any]:
    return {"next_step": "finish"}


def create_workflow() -> CompiledStateGraph:
    workflow = StateGraph(FounderState)

    # Add nodes
    workflow.add_node("planner", planner)
    workflow.add_node("researcher", researcher)
    workflow.add_node("writer", writer)

    # Define simple edges for skeleton verification
    # Planner -> Researcher -> Writer -> END
    workflow.set_entry_point("planner")

    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", END)

    return workflow.compile()
