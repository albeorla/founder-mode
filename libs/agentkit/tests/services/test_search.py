from unittest.mock import MagicMock, patch

import pytest
from agentkit.services.search import TavilySearchService


@patch("agentkit.services.search.TavilyClient")
def test_search_service(mock_tavily: MagicMock) -> None:
    mock_instance = mock_tavily.return_value
    mock_instance.search.return_value = {"results": [{"content": "found", "url": "http://example.com"}]}

    service = TavilySearchService(api_key="test-key")
    results = service.search("query")

    assert len(results) == 1
    assert results[0]["content"] == "found"
    mock_instance.search.assert_called_once_with(query="query", search_depth="advanced")


@patch("agentkit.services.search.get_settings")
def test_search_service_no_key(mock_get_settings: MagicMock) -> None:
    mock_get_settings.return_value = MagicMock(tavily_api_key=None)
    with pytest.raises(ValueError, match="TAVILY_API_KEY"):
        service = TavilySearchService(api_key=None)
        service.search("query")
