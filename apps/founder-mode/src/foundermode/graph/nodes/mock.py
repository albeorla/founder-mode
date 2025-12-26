from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import GraphState


def mock_analyst(state: GraphState) -> GraphState:
    """A mock node that simulates analysis by updating the state with dummy data."""
    print(f"--- Mock Analyst processing query: {state['research_question']} ---")

    # Simulate a draft memo
    draft = InvestmentMemo(
        executive_summary=f"Mock Executive Summary for {state['research_question']}. This is a revolutionary idea.",
        market_analysis="The mock market is valued at $100 Billion.",
        competitive_landscape="Competitors are numerous but lack our mock innovation.",
    )

    # Note: 'plan' key no longer exists in state, so we just update memo_draft
    # We must match the TypedDict structure for return if strictly typed,
    # but GraphState is a TypedDict so we should return partial updates or full state?
    # LangGraph nodes typically return a dict with UPDATES.
    # However, the type hint says -> GraphState.
    # Let's return the full state with updates.

    return {**state, "memo_draft": draft}
