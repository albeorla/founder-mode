from unittest.mock import MagicMock, patch

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
