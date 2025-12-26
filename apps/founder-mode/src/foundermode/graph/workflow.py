from typing import Any, Literal

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from foundermode.domain.state import FounderState
from foundermode.graph.nodes.critic import critic_node
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


def should_revise(state: FounderState) -> Literal["planner", "__end__"]:
    """Decides whether to loop back to the planner based on the critic's verdict."""
    next_step = state["next_step"]
    revision_count = state.get("revision_count", 0)

    if next_step == "reject" and revision_count < 3:
        return "planner"
    return "__end__"


def create_workflow(
    checkpointer: BaseCheckpointSaver[Any] | None = None, interrupt_before: list[str] | None = None
) -> CompiledStateGraph[Any, Any]:
    workflow = StateGraph(FounderState)

    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("critic", critic_node)

    # Define Edges
    workflow.set_entry_point("planner")

    # Conditional edge from planner
    workflow.add_conditional_edges("planner", should_continue)

    # Loop back from researcher to planner
    workflow.add_edge("researcher", "planner")

    # Transition from writer to critic
    workflow.add_edge("writer", "critic")

    # Adversarial loop from critic
    workflow.add_conditional_edges("critic", should_revise, {"planner": "planner", "__end__": END})

    # Default interruption before researcher for HITL
    interrupt = interrupt_before if interrupt_before is not None else ["researcher"]

    return workflow.compile(checkpointer=checkpointer, interrupt_before=interrupt)
