from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from tavily import TavilyClient

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
    chroma: ChromaManager | None = None

    def __init__(self, api_key: str | None = None, chroma: ChromaManager | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.api_key = api_key or settings.tavily_api_key
        self.chroma = chroma or ChromaManager()

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

        client = TavilyClient(api_key=self.api_key)
        response = client.search(query=query, search_depth="advanced")
        results = response.get("results", [])

        # 3. Automatic Upsert: Add new results to ChromaDB
        if self.chroma and results:
            facts_to_add = []
            for r in results:
                facts_to_add.append(
                    ResearchFact(
                        content=r.get("content", ""),
                        source=r.get("url", ""),
                        title=r.get("title"),
                        relevance_score=r.get("score"),
                    )
                )
            self.chroma.add_facts(facts_to_add)

        return results  # type: ignore

    async def _arun(self, query: str) -> list[dict[str, Any]]:
        """Asynchronous execution."""
        return self._run(query)
