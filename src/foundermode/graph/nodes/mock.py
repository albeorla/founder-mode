from foundermode.domain.state import GraphState
from foundermode.domain.schema import ResearchPlan, InvestmentMemo

def mock_analyst(state: GraphState) -> GraphState:
    """A mock node that simulates analysis by updating the state with dummy data."""
    print(f"--- Mock Analyst processing query: {state['query']} ---")
    
    # Simulate a research plan
    plan = ResearchPlan(tasks=[
        "Identify top 3 competitors",
        "Determine average market pricing",
        "Analyze customer pain points in social media"
    ])
    
    # Simulate a draft memo
    draft = InvestmentMemo(
        executive_summary=f"Mock Executive Summary for {state['query']}. This is a revolutionary idea.",
        market_analysis="The mock market is valued at $100 Billion.",
        competitive_landscape="Competitors are numerous but lack our mock innovation."
    )
    
    return {
        **state,
        "plan": plan,
        "draft": draft
    }
