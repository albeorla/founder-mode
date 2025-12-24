from langgraph.graph import END, StateGraph

from foundermode.domain.state import GraphState
from foundermode.graph.nodes.mock import mock_analyst


def create_workflow() -> StateGraph[GraphState]:
    """Creates the LangGraph workflow."""
    workflow = StateGraph(GraphState)

    workflow.add_node("analyst", mock_analyst)

    # Define the graph edges
    workflow.set_entry_point("analyst")
    workflow.add_edge("analyst", END)

    return workflow
