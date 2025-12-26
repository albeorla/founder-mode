from unittest.mock import AsyncMock, patch

import pytest
from agentkit.services.extraction import ExtractionService


@pytest.mark.asyncio
@patch("agentkit.services.extraction.httpx.AsyncClient")
async def test_extraction_service_http_fallback(mock_client: AsyncMock) -> None:
    # Mock HTTP response
    mock_response = AsyncMock()
    mock_response.text = "<html><body><h1>Title</h1><p>Main content here...</p></body></html>"
    mock_response.raise_for_status = AsyncMock()

    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

    service = ExtractionService()
    result = await service.extract("http://example.com", use_playwright=False)

    assert "Title" in result
    assert "Main content here" in result


@pytest.mark.asyncio
@patch("agentkit.services.extraction.ExtractionService._scrape_with_playwright")
async def test_extraction_service_playwright(mock_playwright: AsyncMock) -> None:
    mock_playwright.return_value = "<html><body>Dynamic Content</body></html>"

    service = ExtractionService()
    result = await service.extract("http://example.com", use_playwright=True)

    assert "Dynamic Content" in result
    mock_playwright.assert_called_once()
