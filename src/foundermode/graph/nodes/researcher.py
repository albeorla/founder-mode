import asyncio
import logging
from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from foundermode.config import settings
from foundermode.domain.schema import ResearchFact
from foundermode.domain.state import FounderState
from foundermode.memory.vector_store import ChromaManager
from foundermode.tools.scrape import deep_scrape_url
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


class URLSelection(BaseModel):
    urls: list[str] = Field(..., description="List of 1-3 URLs that deserve deep scraping for more detail.")
    reason: str = Field(..., description="Why these specific URLs were selected.")


selector_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a Research Lead. Review these search results and identify 1-3 URLs that likely contain
    the most detailed quantitative data (pricing, financials, deep feature lists) for our topic.
    Priority: Official pricing pages, SEC filings, deep industry reports, detailed product documentation.""",
        ),
        ("human", "Search Results for '{topic}':\n{search_results}"),
    ]
)


extractor_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a Research Assistant. Your job is to extract high-signal facts from the provided text.
    Ignore generic fluff. We want numbers, dates, competitor names, and pricing info.
    Extract the key facts and assign a relevance score (0.0 - 1.0).""",
        ),
        ("human", "Text to analyze:\n{text}"),
    ]
)


class FactList(BaseModel):
    facts: list[EvaluatedFact]


def get_selector_chain() -> Any:
    if not settings.openai_api_key:
        return None
    llm = ChatOpenAI(model=settings.model_name, temperature=0, openai_api_key=settings.openai_api_key)
    return selector_prompt | llm.with_structured_output(URLSelection)


def get_extractor_chain() -> Any:
    if not settings.openai_api_key:
        return None
    llm = ChatOpenAI(model=settings.model_name, temperature=0, openai_api_key=settings.openai_api_key)
    return extractor_prompt | llm.with_structured_output(FactList)


def researcher_node(state: FounderState) -> dict[str, Any]:
    """
    Executes the research step with deep scraping capabilities.
    """
    topic = state.get("research_topic") or state["research_question"]
    logger.info(f"Researcher Node: Searching for '{topic}'")

    # Initialize tools
    search_tool = TavilySearch(api_key=settings.tavily_api_key)
    memory = ChromaManager()

    # 1. Search Stage
    try:
        raw_results = search_tool.invoke(topic)
        if isinstance(raw_results, str):
            raw_results = [{"content": raw_results, "url": "none", "title": "Search Result"}]

        # Filter out API Errors
        valid_results = []
        if raw_results:
            for r in raw_results:
                content = r.get("content", "").lower()
                if "unauthorized" in content or "invalid api key" in content or "error searching" in content:
                    continue
                valid_results.append(r)
        raw_results = valid_results if valid_results else None
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raw_results = None

    facts: list[ResearchFact] = []

    # 2. Deep Scrape Stage (Optional based on selection)
    selector_chain = get_selector_chain()
    scraped_urls = []

    if raw_results and selector_chain:
        try:
            results_str = "\n".join(
                [f"URL: {r.get('url')}\nTitle: {r.get('title')}\nSnippet: {r.get('content')}\n---" for r in raw_results]
            )
            selection = selector_chain.invoke({"topic": topic, "search_results": results_str})
            scraped_urls = selection.urls
            logger.info(f"Selected {len(scraped_urls)} URLs for deep scraping.")
        except Exception as e:
            logger.warning(f"URL selection failed: {e}")

    # Execute scraping
    scraped_contents = []
    for url in scraped_urls:
        try:
            # We don't use Playwright by default unless specifically needed
            content = asyncio.run(deep_scrape_url.ainvoke({"url": url}))
            if content and "Error scraping" not in content:
                scraped_contents.append({"url": url, "text": content})
                # Add full text to memory with chunking
                memory.add_scraped_text(url, content, title=f"Deep Scrape: {topic}")
        except Exception as e:
            logger.error(f"Scraping failed for {url}: {e}")

    # 3. Extraction Stage
    extractor_chain = get_extractor_chain()

    # Process scraped contents first
    for item in scraped_contents:
        if extractor_chain:
            try:
                # Extract structured facts from full text
                # We take a large chunk of the text (context limits apply)
                text_to_analyze = item["text"][:10000]  # Safe limit for gpt-4o
                extraction = extractor_chain.invoke({"text": text_to_analyze})
                for ef in extraction.facts:
                    if ef.relevance_score > 0.5:
                        facts.append(
                            ResearchFact(
                                content=ef.content,
                                source=item["url"],
                                title=f"Deep Scrape: {topic}",
                                relevance=ef.relevance_score,
                            )
                        )
            except Exception as e:
                logger.error(f"Extraction failed for scraped content: {e}")

    # Fallback to snippets if facts are still low
    if len(facts) < 3 and raw_results:
        # Use existing extraction logic from snippets
        results_str = "\n".join([f"Source: {r.get('url')}\nContent: {r.get('content')}\n---" for r in raw_results])
        if extractor_chain:
            try:
                extraction = extractor_chain.invoke({"text": results_str})
                for ef in extraction.facts:
                    if ef.relevance_score > 0.4:
                        facts.append(
                            ResearchFact(
                                content=ef.content,
                                source=ef.source_url,
                                title=f"Snippet: {topic}",
                                relevance=ef.relevance_score,
                            )
                        )
            except Exception as e:
                logger.error(f"Snippet extraction failed: {e}")

    # Safety Fallbacks
    if not facts and raw_results:
        for r in raw_results:
            facts.append(
                ResearchFact(
                    content=r.get("content", ""),
                    source=r.get("url", "none"),
                    title=f"Raw Snippet: {topic}",
                    relevance_score=1.0,
                )
            )
    elif not facts:
        facts.append(
            ResearchFact(
                content=f"Mock Fact: {topic} is a high-growth sector.",
                source="Mock Data",
                title=f"Mock Search: {topic}",
                relevance_score=0.5,
            )
        )

    # Store in memory
    memory.add_facts(facts)
    logger.info(f"Added {len(facts)} facts to memory.")

    return {"research_facts": facts, "next_step": "planner"}
