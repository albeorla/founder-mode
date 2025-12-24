from typing import Any

from foundermode.domain.schema import ResearchFact
from foundermode.domain.state import FounderState
from foundermode.memory.vector_store import ChromaManager
from foundermode.tools.search import TavilySearch

# We can reuse the planner LLM or a new one for extraction.
# For simplicity, we'll just wrap the search result in a single fact for now,
# or split by newlines if the tool returns a list.
# Tavily usually returns a string or a JSON. The tool wrapper returns a string.


def researcher_node(state: FounderState) -> dict[str, Any]:
    """
    Executes the research step.
    """
    topic = state.get("research_topic") or state["research_question"]

    # Initialize tools
    search_tool = TavilySearch()
    memory = ChromaManager()

    # Execute search
    try:
        search_result = search_tool.invoke(topic)
    except Exception as e:
        search_result = f"Error searching for {topic}: {e}"

    # Process result into a Fact
    # In a production system, we would use an LLM to parse this into atomic facts.
    # Here we treat the summary as one fact.
    fact = ResearchFact(
        content=str(search_result),
        source="Tavily",
        title=f"Search: {topic}",
        relevance_score=1.0,  # Assume relevant if found
    )

    # Store in memory
    memory.add_facts([fact])

    # Update state
    # We return the NEW fact to be added to the list (reducer handles append)
    return {"research_facts": [fact], "next_step": "planner"}
