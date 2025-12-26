from typing import Any, cast

from tavily import TavilyClient

from agentkit.infra.config import get_settings


class TavilySearchService:
    """Service for performing web searches using Tavily."""

    def __init__(self, api_key: str | None = None):
        settings = get_settings()
        self.api_key = api_key or settings.tavily_api_key

    def search(self, query: str, search_depth: str = "advanced") -> list[dict[str, Any]]:
        """Perform a synchronous search."""
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY must be set.")

        client = TavilyClient(api_key=self.api_key)
        response = client.search(query=query, search_depth=search_depth)
        return cast(list[dict[str, Any]], response.get("results", []))

    async def asearch(self, query: str, search_depth: str = "advanced") -> list[dict[str, Any]]:
        """Perform an asynchronous search. Currently wraps sync search."""
        # In a real production scenario, we'd use an async client
        import asyncio

        return await asyncio.to_thread(self.search, query, search_depth)
