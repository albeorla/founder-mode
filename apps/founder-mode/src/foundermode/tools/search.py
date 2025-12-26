from typing import Any

from agentkit.services.search import TavilySearchService
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from foundermode.config import settings
from foundermode.domain.schema import ResearchFact
from foundermode.memory.vector_store import ChromaManager


class TavilySearchInput(BaseModel):
    query: str = Field(description="The search query to execute")


class TavilySearch(BaseTool):  # type: ignore
    """
    A tool that uses the Tavily API to perform web searches,
    integrated with ChromaDB for working memory.
    """

    name: str = "tavily_search"
    description: str = "Search the web for information about companies, markets, and business ideas."
    args_schema: type[BaseModel] = TavilySearchInput
    api_key: str | None = None
    chroma: Any = Field(default_factory=ChromaManager)

    def __init__(self, **kwargs: Any) -> None:
        if "api_key" not in kwargs:
            kwargs["api_key"] = settings.tavily_api_key
        super().__init__(**kwargs)

    def _run(self, query: str) -> list[dict[str, Any]]:
        """Execute the search tool with memory integration."""
        # 1. Search-as-Memory: Check ChromaDB first
        if self.chroma:
            existing_facts = self.chroma.query_similar(query, k=3)
            if existing_facts:
                return [{"content": f.content, "url": f.source, "title": f.title} for f in existing_facts]

        # 2. Live Search: Call Tavily
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY must be set in environment or passed to the tool.")

        service = TavilySearchService(api_key=self.api_key)
        results = service.search(query=query, search_depth="advanced")

        # 3. Automatic Upsert: Add new results to ChromaDB
        if self.chroma and results:
            facts_to_add = []
            for r in results:
                content = r.get("content", "")
                # Skip errors or very short/useless content
                if "error" in content.lower() or "unauthorized" in content.lower() or len(content) < 20:
                    continue

                facts_to_add.append(
                    ResearchFact(
                        content=content,
                        source=r.get("url", ""),
                        title=r.get("title"),
                        relevance_score=r.get("score"),
                    )
                )
            if facts_to_add:
                self.chroma.add_facts(facts_to_add)

        return results  # type: ignore

    async def _arun(self, query: str) -> list[dict[str, Any]]:
        """Asynchronous execution."""
        return self._run(query)
