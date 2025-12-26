from unittest.mock import AsyncMock, patch

import httpx
import pytest
import respx

from foundermode.tools.scrape import deep_scrape_url

# HTML Constants for testing
SIMPLE_HTML = "<html><body><h1>Title</h1><p>Main content paragraph.</p></body></html>"
SHORT_HTML = "<html><body><p>Short content.</p></body></html>"
SCRIPT_HTML = "<html><body><script>var x=1;</script><h1>Real Content</h1></body></html>"
PLAYWRIGHT_HTML = "<html><body><div id='app'>Dynamic Content</div></body></html>"


@pytest.mark.asyncio  # type: ignore
@respx.mock  # type: ignore
async def test_deep_scrape_readability_success() -> None:
    """Test that Readability extracts content correctly."""
    url = "https://example.com/readability"
    respx.get(url).mock(return_value=httpx.Response(200, text=SIMPLE_HTML))

    result = await deep_scrape_url.ainvoke({"url": url})

    # Readability usually preserves the title and p tags in summary,
    # but the tool converts it to text.
    assert "Title" in result
    assert "Main content paragraph." in result


@pytest.mark.asyncio  # type: ignore
@respx.mock  # type: ignore
async def test_deep_scrape_fallback_bs4() -> None:
    """Test fallback to BS4 when Readability returns short content."""
    url = "https://example.com/fallback"
    # Readability might strip too much from very short/malformed HTML or if we force it.
    # Here we simulate an HTML where readability might be minimal,
    # but let's trust the logic: if len < 500, it falls back.
    # SIMPLE_HTML is definitely < 500 chars.

    respx.get(url).mock(return_value=httpx.Response(200, text=SHORT_HTML))

    result = await deep_scrape_url.ainvoke({"url": url})

    # Should contain the text from p tag
    assert "Short content." in result


@pytest.mark.asyncio  # type: ignore
async def test_deep_scrape_playwright() -> None:
    """Test Playwright scraping path."""
    url = "https://example.com/dynamic"

    # Mock playwright
    with patch("foundermode.tools.scrape.scrape_with_playwright", new_callable=AsyncMock) as mock_pw:
        mock_pw.return_value = PLAYWRIGHT_HTML

        # We need to mock fetch_html as well if playwright fails, but here it succeeds.
        # However, the tool calls scrape_with_readability on the result of playwright.

        result = await deep_scrape_url.ainvoke({"url": url, "use_playwright": True})

        mock_pw.assert_called_once_with(url)
        assert "Dynamic Content" in result


@pytest.mark.asyncio  # type: ignore
@respx.mock  # type: ignore
async def test_deep_scrape_fetch_error() -> None:
    """Test handling of fetch errors."""
    url = "https://example.com/error"
    respx.get(url).mock(return_value=httpx.Response(404))

    result = await deep_scrape_url.ainvoke({"url": url})

    assert "Failed to retrieve content" in result or "Error scraping" in result


@pytest.mark.asyncio  # type: ignore
async def test_deep_scrape_playwright_failure_fallback() -> None:
    """Test that if Playwright fails, it falls back to normal fetch."""
    url = "https://example.com/pw-fail"

    with patch("foundermode.tools.scrape.scrape_with_playwright", new_callable=AsyncMock) as mock_pw:
        mock_pw.side_effect = Exception("Playwright crashed")

        # Mock normal fetch using respx inside the patch context
        with respx.mock:
            respx.get(url).mock(return_value=httpx.Response(200, text=SIMPLE_HTML))

            result = await deep_scrape_url.ainvoke({"url": url, "use_playwright": True})

            mock_pw.assert_called_once()
            # Should have fallen back to SIMPLE_HTML content
            assert "Main content paragraph." in result
