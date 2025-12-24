from typing import Any

from foundermode.domain.schema import ResearchFact
from foundermode.domain.state import FounderState
from foundermode.memory.vector_store import ChromaManager
from foundermode.tools.search import TavilySearch


def researcher_node(state: FounderState) -> dict[str, Any]:
    """
    Executes the research step.
    Supports dynamic fallback to mock data if search fails.
    """
    topic = state.get("research_topic") or state["research_question"]

    # Initialize tools
    search_tool = TavilySearch()
    memory = ChromaManager()

    # Execute search
    try:
        search_results = search_tool.invoke(topic)
        # If search_results is a string (error message or single result), wrap it
        if isinstance(search_results, str):
            search_results = [{"content": search_results, "url": "none", "title": "Search Result"}]
    except Exception as e:
        print(f"Researcher search failed, falling back to mock: {e}")
        search_results = None

    # Process result into Facts
    facts: list[ResearchFact] = []

    if search_results:
        for r in search_results:
            facts.append(
                ResearchFact(
                    content=r.get("content", ""),
                    source=r.get("url", "none"),
                    title=r.get("title", f"Search: {topic}"),
                    relevance_score=r.get("score", 1.0),
                )
            )
    else:
        # Mock Fallback Logic
        facts.append(
            ResearchFact(
                content=f"Mock Fact: {topic} is a high-growth sector with significant potential.",
                source="Mock Data",
                title=f"Mock Search: {topic}",
                relevance_score=0.5,
            )
        )

    # Store in memory
    memory.add_facts(facts)

    # Update state
    return {"research_facts": facts, "next_step": "planner"}
