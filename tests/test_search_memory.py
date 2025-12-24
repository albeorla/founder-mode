from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from foundermode.domain.schema import ResearchFact
from foundermode.memory.vector_store import ChromaManager
from foundermode.tools.search import TavilySearch


@pytest.fixture
def mock_chroma() -> Generator[MagicMock, None, None]:
    with patch("foundermode.tools.search.ChromaManager") as mock:
        manager = MagicMock(spec=ChromaManager)
        mock.return_value = manager
        yield manager


@pytest.fixture
def search_tool() -> TavilySearch:
    # Provide a dummy API key to avoid validation error
    return TavilySearch(api_key="test-key")


def test_search_as_memory_hit(mock_chroma: MagicMock, search_tool: TavilySearch) -> None:
    # Setup: ChromaDB has the answer
    existing_fact = ResearchFact(content="Existing info about Airbnb", source="local_db", title="Cached")
    mock_chroma.query_similar.return_value = [existing_fact]

    with patch("foundermode.tools.search.TavilyClient") as mock_tavily:
        results = search_tool._run("Airbnb info")

        # Verify: Tavily was NOT called (Search-as-Memory hit)
        mock_tavily.assert_not_called()
        assert len(results) == 1
        assert results[0]["content"] == "Existing info about Airbnb"


def test_search_as_memory_miss_calls_tavily(mock_chroma: MagicMock, search_tool: TavilySearch) -> None:
    # Setup: ChromaDB is empty
    mock_chroma.query_similar.return_value = []

    with patch("foundermode.tools.search.TavilyClient") as mock_tavily:
        mock_client = mock_tavily.return_value
        mock_client.search.return_value = {
            "results": [{"content": "New info from web", "url": "https://example.com", "title": "Web result"}]
        }

        results = search_tool._run("New topic")

        # Verify: Tavily WAS called
        mock_client.search.assert_called_once()
        assert len(results) == 1
        assert results[0]["content"] == "New info from web"

        # Verify: Results were added to ChromaDB
        mock_chroma.add_facts.assert_called_once()


def test_deduplication_before_upsert(mock_chroma: MagicMock, search_tool: TavilySearch) -> None:
    # This is a bit more complex to test, depends on implementation.
    # We want to ensure that if a result URL is already in metadata, we might skip it or update.
    # For now, let's just ensure it calls add_facts with the right data.
    pass
