from unittest.mock import MagicMock, patch

import pytest

from foundermode.tools.search import TavilySearch


def test_tavily_search_input_schema() -> None:
    tool = TavilySearch()
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

    tool = TavilySearch(api_key="test_key")
    results = tool._run(query="test query")

    assert len(results) == 2
    assert results[0]["title"] == "Result 1"
    mock_client.search.assert_called_once_with(query="test query", search_depth="advanced")


def test_tavily_search_missing_api_key() -> None:
    with patch.dict("os.environ", {}, clear=True):
        tool = TavilySearch()
        with pytest.raises(ValueError, match="TAVILY_API_KEY must be set"):
            tool._run(query="test")


@pytest.mark.asyncio  # type: ignore
@patch("foundermode.tools.search.TavilyClient")
async def test_tavily_search_arun(mock_client_class: MagicMock) -> None:
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    mock_client.search.return_value = {"results": [{"title": "Async Result"}]}

    tool = TavilySearch(api_key="test_key")
    results = await tool._arun(query="test async")

    assert results[0]["title"] == "Async Result"
