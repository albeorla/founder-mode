import logging
from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from foundermode.config import settings
from foundermode.domain.schema import ResearchFact
from foundermode.domain.state import FounderState
from foundermode.memory.vector_store import ChromaManager
from foundermode.tools.search import TavilySearch

logger = logging.getLogger(__name__)


class EvaluatedFact(BaseModel):
    content: str = Field(..., description="A standalone, high-signal fact extracted from search results.")
    source_url: str = Field(..., description="The URL this fact came from.")
    relevance_score: float = Field(
        ...,
        description=(
            "0.0 to 1.0 score of how valuable this fact is for investment due diligence (favors numbers, names, dates)."
        ),
    )


extractor_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a Research Assistant. Your job is to extract high-signal facts from search results.
    Ignore generic fluff. We want numbers, dates, competitor names, and pricing info.
    For each result, extract the key fact and assign a relevance score (0.0 - 1.0).
    If a result contains no useful info, skip it.""",
        ),
        ("human", "Search Results:\n{search_results}"),
    ]
)


class FactList(BaseModel):
    facts: list[EvaluatedFact]


def get_extractor_chain() -> Any:
    if not settings.openai_api_key:
        return None
    llm = ChatOpenAI(model=settings.model_name, temperature=0, openai_api_key=settings.openai_api_key)
    return extractor_prompt | llm.with_structured_output(FactList)


def researcher_node(state: FounderState) -> dict[str, Any]:
    """
    Executes the research step.
    Supports dynamic fallback to mock data if search fails.
    """
    topic = state.get("research_topic") or state["research_question"]
    logger.info(f"Researcher Node: Searching for '{topic}'")

    # Initialize tools
    search_tool = TavilySearch()
    memory = ChromaManager()

    # Execute search
    try:
        raw_results = search_tool.invoke(topic)
        # If search_results is a string (error message or single result), wrap it
        if isinstance(raw_results, str):
            raw_results = [{"content": raw_results, "url": "none", "title": "Search Result"}]

        # Filter out API Errors (e.g. "Unauthorized", "invalid API key")
        valid_results = []
        if raw_results:
            for r in raw_results:
                content = r.get("content", "").lower()
                if "unauthorized" in content or "invalid api key" in content or "error searching" in content:
                    logger.warning(f"Detected API error in search result: {content[:50]}...")
                    continue
                valid_results.append(r)

        raw_results = valid_results if valid_results else None
        logger.debug(f"Search returned {len(raw_results) if raw_results else 0} valid results.")
    except Exception as e:
        logger.error(f"Researcher search failed: {e}", exc_info=True)
        print(f"Researcher search failed, falling back to mock: {e}")
        raw_results = None

    # Process result into Facts
    facts: list[ResearchFact] = []

    chain = get_extractor_chain()

    if raw_results and chain:
        # LLM-based extraction
        try:
            logger.debug("Attempting LLM-based fact extraction.")
            # Prepare input for LLM
            # We map the raw dicts to a string representation
            results_str = "\n".join([f"Source: {r.get('url')}\nContent: {r.get('content')}\n---" for r in raw_results])

            extraction = chain.invoke({"search_results": results_str})

            if extraction and extraction.facts:
                for ef in extraction.facts:
                    if ef.relevance_score > 0.4:  # Filter low relevance
                        facts.append(
                            ResearchFact(
                                content=ef.content,
                                source=ef.source_url,
                                title=f"Fact from {topic}",
                                relevance=ef.relevance_score,
                            )
                        )
                logger.info(f"LLM extracted {len(facts)} high-signal facts.")
            else:
                logger.warning("LLM extraction returned no facts.")
        except Exception as e:
            logger.error(f"Fact extraction failed: {e}. Falling back to raw.", exc_info=True)
            print(f"Fact extraction failed: {e}. Falling back to raw.")
            # Fallback to raw if LLM fails
            for r in raw_results:
                facts.append(
                    ResearchFact(
                        content=r.get("content", ""),
                        source=r.get("url", "none"),
                        title=r.get("title", f"Search: {topic}"),
                        relevance_score=r.get("score", 1.0),
                    )
                )

    elif raw_results:
        # No LLM chain available, use raw
        logger.info("LLM extraction unavailable. Using raw results.")
        for r in raw_results:
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
        logger.info("Researcher Node: Using Mock Fallback Logic (No raw results).")
        facts.append(
            ResearchFact(
                content=f"Mock Fact: {topic} is a high-growth sector with significant potential.",
                source="Mock Data",
                title=f"Mock Search: {topic}",
                relevance_score=0.5,
            )
        )

    # Final Safety Net: If facts is still empty (e.g. LLM filtered everything out), use raw
    if not facts and raw_results:
        logger.warning("Facts empty after processing. Fallback to raw results to ensure progress.")
        for r in raw_results:
            facts.append(
                ResearchFact(
                    content=r.get("content", ""),
                    source=r.get("url", "none"),
                    title=r.get("title", f"Search: {topic}"),
                    relevance_score=r.get("score", 1.0),
                )
            )
    elif not facts:
        # Double safety: Mock if still empty
        logger.warning("Facts empty after all fallbacks. Injecting safety mock fact.")
        facts.append(
            ResearchFact(
                content=f"Mock Fact (Fallback): {topic}",
                source="System",
                title=f"Mock Search: {topic}",
                relevance_score=0.1,
            )
        )

    # Store in memory
    memory.add_facts(facts)
    logger.debug(f"Added {len(facts)} facts to memory.")

    # Update state
    return {"research_facts": facts, "next_step": "planner"}
