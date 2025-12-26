from unittest.mock import MagicMock, patch

import pytest

from foundermode.domain.schema import ResearchFact
from foundermode.tools.search import TavilySearch


@pytest.fixture
def mock_chroma() -> MagicMock:
    return MagicMock()


@pytest.fixture
def search_tool(mock_chroma: MagicMock) -> TavilySearch:
    # We pass mock_chroma to override default initialization
    return TavilySearch(api_key="test-key", chroma=mock_chroma)


def test_search_as_memory_hit_skips_tavily(mock_chroma: MagicMock, search_tool: TavilySearch) -> None:
    # Setup: ChromaDB has the answer
    fact = ResearchFact(content="Known fact from memory", source="http://old", title="Old")
    mock_chroma.query_similar.return_value = [fact]

    with patch("foundermode.tools.search.TavilySearchService") as mock_service:
        results = search_tool._run("Existing topic")

        # Verify: Tavily was NOT called
        mock_service.assert_not_called()
        assert len(results) == 1
        assert results[0]["content"] == "Known fact from memory"


def test_search_as_memory_miss_calls_tavily(mock_chroma: MagicMock, search_tool: TavilySearch) -> None:
    # Setup: ChromaDB is empty
    mock_chroma.query_similar.return_value = []

    with patch("foundermode.tools.search.TavilySearchService") as mock_service_cls:
        mock_service = mock_service_cls.return_value
        mock_service.search.return_value = [
            {
                "content": "This is a long enough content to pass the filter of twenty characters.",
                "url": "https://example.com",
                "title": "Web result",
                "score": 0.9,
            }
        ]

        results = search_tool._run("New topic")

        # Verify: Tavily WAS called
        mock_service.search.assert_called_once()
        assert len(results) == 1
        assert "long enough" in results[0]["content"]

        # Verify: Results were added to ChromaDB
        mock_chroma.add_facts.assert_called_once()


def test_search_as_memory_disabled_without_chroma() -> None:
    # Tool without chroma manager
    tool = TavilySearch(api_key="test-key", chroma=None)

    with patch("foundermode.tools.search.TavilySearchService") as mock_service_cls:
        mock_service = mock_service_cls.return_value
        mock_service.search.return_value = []

        tool._run("Any topic")
        mock_service.search.assert_called_once()
