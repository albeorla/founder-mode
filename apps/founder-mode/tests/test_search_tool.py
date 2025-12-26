from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from foundermode.tools.search import TavilySearch


@pytest.fixture(autouse=True)
def mock_chroma() -> Generator[MagicMock, None, None]:
    with patch("foundermode.tools.search.ChromaManager") as mock:
        manager = MagicMock()
        mock.return_value = manager
        manager.query_similar.return_value = []
        yield manager


def test_tavily_search_input_schema() -> None:
    # We need to mock ChromaManager even for schema test because __init__ calls it
    with patch("foundermode.tools.search.ChromaManager"):
        tool = TavilySearch(api_key="test")
        assert tool.name == "tavily_search"
        assert "query" in tool.args_schema.model_fields


@patch("foundermode.tools.search.TavilyClient")
def test_tavily_search_run(mock_client_class: MagicMock) -> None:
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    mock_client.search.return_value = {
        "results": [
            {"title": "Result 1", "url": "https://example.com/1", "content": "Content 1"},
            {"title": "Result 2", "url": "https://example.com/2", "content": "Content 2"},
        ]
    }

    # Explicitly pass a mock chroma to avoid any __init__ issues
    mock_c = MagicMock()
    mock_c.query_similar.return_value = []

    tool = TavilySearch(api_key="test_key", chroma=mock_c)
    results = tool._run(query="test query")

    assert len(results) == 2
    assert results[0]["title"] == "Result 1"
    mock_client.search.assert_called_once_with(query="test query", search_depth="advanced")


def test_tavily_search_missing_api_key() -> None:
    with patch("foundermode.tools.search.settings") as mock_settings:
        mock_settings.tavily_api_key = None
        # Ensure chroma is mocked to return nothing so it proceeds to live search
        mock_c = MagicMock()
        mock_c.query_similar.return_value = []

        tool = TavilySearch(api_key=None, chroma=mock_c)
        with pytest.raises(ValueError, match="TAVILY_API_KEY must be set"):
            tool._run(query="test")


@pytest.mark.asyncio  # type: ignore
@patch("foundermode.tools.search.TavilyClient")
async def test_tavily_search_arun(mock_client_class: MagicMock) -> None:
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    mock_client.search.return_value = {"results": [{"title": "Async Result"}]}

    mock_c = MagicMock()
    mock_c.query_similar.return_value = []

    tool = TavilySearch(api_key="test_key", chroma=mock_c)
    results = await tool._arun(query="test async")

    assert results[0]["title"] == "Async Result"
