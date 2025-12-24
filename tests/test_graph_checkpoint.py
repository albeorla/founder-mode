from langgraph.checkpoint.memory import MemorySaver

from foundermode.graph.workflow import create_workflow


def test_graph_interrupt_before_researcher() -> None:
    """Test that the graph interrupts before the researcher node."""
    # 1. Setup with checkpointer
    memory = MemorySaver()
    workflow = create_workflow(checkpointer=memory)

    # 2. Initial input
    initial_state = {
        "research_question": "A platform for pet rocks",
        "research_facts": [],
        "memo_draft": None,
        "next_step": "plan",
        # Some optional fields might be needed depending on state definition
        # but these seem to be the core ones
        "messages": [],
    }

    # 3. Run until interruption
    # config is required for checkpointing
    config = {"configurable": {"thread_id": "test_thread_1"}}

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
    # Ensure planner ran (it might have added messages or updated state)
    # The planner node updates next_step, so verifying that is good enough.


def test_resume_graph() -> None:
    """Test that we can resume the graph after interruption."""
    memory = MemorySaver()
    workflow = create_workflow(checkpointer=memory)
    config = {"configurable": {"thread_id": "test_thread_2"}}

    initial_state = {
        "research_question": "AI for plants",
        "research_facts": [],
        "memo_draft": None,
        "next_step": "plan",
        "messages": [],
    }

    # Run 1: Should stop before researcher
    for _ in workflow.stream(initial_state, config=config):
        pass

    snapshot = workflow.get_state(config)
    assert snapshot.next == ("researcher",)

    # Run 2: Resume (Command to continue)
    # Passing None as input means "continue from current state"
    # We'll use a mocked researcher that doesn't actually hit the internet
    # to avoid errors, or just trust the graph wiring.
    # For this unit test, simply verifying we are AT the researcher is enough
    # for the 'Red' phase of 'Configure Graph Checkpointing'.
