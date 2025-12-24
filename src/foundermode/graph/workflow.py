from typing import Literal

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from foundermode.domain.state import FounderState
from foundermode.graph.nodes.planner import planner_node
from foundermode.graph.nodes.researcher import researcher_node
from foundermode.graph.nodes.writer import writer_node


def should_continue(state: FounderState) -> Literal["researcher", "writer"]:
    """Decides the next node based on the planner's decision."""
    next_step = state["next_step"]
    if next_step == "research":
        return "researcher"
    elif next_step == "write":
        return "writer"
    else:
        # Fallback or error handling
        return "writer"


def create_workflow(checkpointer: BaseCheckpointSaver | None = None) -> CompiledStateGraph:
    workflow = StateGraph(FounderState)

    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)

    # Define Edges
    workflow.set_entry_point("planner")

    # Conditional edge from planner
    workflow.add_conditional_edges("planner", should_continue)

    # Loop back from researcher to planner
    workflow.add_edge("researcher", "planner")

    # End after writer
    workflow.add_edge("writer", END)

    return workflow.compile(checkpointer=checkpointer, interrupt_before=["researcher"])
