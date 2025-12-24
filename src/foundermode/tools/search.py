import os
from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from tavily import TavilyClient


class TavilySearchInput(BaseModel):
    query: str = Field(description="The search query to execute")


class TavilySearch(BaseTool):  # type: ignore[misc]
    """Tool for performing web searches using the Tavily API."""

    name: str = "tavily_search"
    description: str = "Search the web for information about companies, markets, and business ideas."
    args_schema: type[BaseModel] = TavilySearchInput
    api_key: str | None = None

    def __init__(self, api_key: str | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")

    def _run(self, query: str) -> list[dict[str, Any]]:
        """Execute the search tool."""
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY must be set in environment or passed to the tool.")

        client = TavilyClient(api_key=self.api_key)
        response = client.search(query=query, search_depth="advanced")

        results = response.get("results", [])
        return results  # type: ignore

    async def _arun(self, query: str) -> list[dict[str, Any]]:
        """Asynchronous execution (not implemented)."""
        # Tavily python client is synchronous, but we can implement async if needed using httpx
        return self._run(query)
