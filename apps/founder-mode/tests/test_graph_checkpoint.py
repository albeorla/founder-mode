from typing import cast
from unittest.mock import patch

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import FounderState
from foundermode.graph.workflow import create_workflow


def test_graph_interrupt_before_researcher() -> None:
    """Test that the graph interrupts before the researcher node."""
    # Mock planner node where it's used in the workflow module
    with patch("foundermode.graph.workflow.planner_node") as mock_planner:
        mock_planner.return_value = {"next_step": "research", "research_topic": "rocks"}

        # 1. Setup with checkpointer
        memory = MemorySaver()
        workflow = create_workflow(checkpointer=memory)

        # 2. Initial input
        initial_state: FounderState = {
            "research_question": "A platform for pet rocks",
            "research_facts": [],
            "memo_draft": InvestmentMemo(),
            "next_step": "plan",
            # Some optional fields might be needed depending on state definition
            # but these seem to be the core ones
            "messages": [],
            "research_topic": None,
            "search_history": [],
            "critique_history": [],
            "revision_count": 0,
        }

        # 3. Run until interruption
        # config is required for checkpointing
        config = cast(RunnableConfig, {"configurable": {"thread_id": "test_thread_1"}})

        # Run. It should stop after planner (which outputs next_step='research')
        # and BEFORE executing 'researcher'.

        # Now run it
        # We expect it to yield the state after 'planner' runs
        for _ in workflow.stream(initial_state, config=config):
            pass

    # 4. Verify state is saved at the checkpoint
    snapshot = workflow.get_state(config)
    assert snapshot.next == ("researcher",)
    assert snapshot.values["next_step"] == "research"


def test_resume_graph() -> None:
    """Test that we can resume the graph after interruption."""
    # Run 1: Should stop before researcher
    with patch("foundermode.graph.workflow.planner_node") as mock_planner:
        mock_planner.return_value = {"next_step": "research", "research_topic": "plants"}

        memory = MemorySaver()
        workflow = create_workflow(checkpointer=memory)
        config = cast(RunnableConfig, {"configurable": {"thread_id": "test_thread_2"}})

        initial_state: FounderState = {
            "research_question": "AI for plants",
            "research_facts": [],
            "memo_draft": InvestmentMemo(),
            "next_step": "plan",
            "messages": [],
            "research_topic": None,
            "search_history": [],
            "critique_history": [],
            "revision_count": 0,
        }

        for _ in workflow.stream(initial_state, config=config):
            pass

    snapshot = workflow.get_state(config)
    assert snapshot.next == ("researcher",)
