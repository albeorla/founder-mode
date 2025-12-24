from foundermode.domain.schema import InvestmentMemo, ResearchPlan, ResearchTask
from foundermode.domain.state import GraphState


def mock_analyst(state: GraphState) -> GraphState:
    """A mock node that simulates analysis by updating the state with dummy data."""
    print(f"--- Mock Analyst processing query: {state['query']} ---")

    # Simulate a research plan with ResearchTask objects
    plan = ResearchPlan(
        tasks=[
            ResearchTask(question="Identify top 3 competitors"),
            ResearchTask(question="Determine average market pricing"),
            ResearchTask(question="Analyze customer pain points in social media"),
        ]
    )

    # Simulate a draft memo
    draft = InvestmentMemo(
        executive_summary=f"Mock Executive Summary for {state['query']}. This is a revolutionary idea.",
        market_analysis="The mock market is valued at $100 Billion.",
        competitive_landscape="Competitors are numerous but lack our mock innovation.",
    )

    return {**state, "plan": plan, "draft": draft}
