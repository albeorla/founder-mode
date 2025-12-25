import httpx
import pytest
import respx

from foundermode.tools.scrape import scrape_url


@pytest.mark.asyncio  # type: ignore
@respx.mock  # type: ignore
async def test_scrape_url_success() -> None:
    url = "https://example.com"
    respx.get(url).mock(return_value=httpx.Response(200, text="<html><body><h1>Hello World</h1></body></html>"))

    # scrape_url is a StructuredTool, so we must use ainvoke
    text = await scrape_url.ainvoke(url)
    assert "Hello World" in text


@pytest.mark.asyncio  # type: ignore
@respx.mock  # type: ignore
async def test_scrape_url_failure() -> None:
    url = "https://example.com/notfound"
    # scrape_url is a StructuredTool, so we must use ainvoke
    text = await scrape_url.ainvoke(url)
    assert "Error scraping" in text


@pytest.mark.asyncio  # type: ignore
@respx.mock  # type: ignore
async def test_scrape_url_strips_scripts() -> None:
    url = "https://example.com/js"
    html = "<html><body><script>alert(1)</script><h1>Hello World</h1></body></html>"
    respx.get(url).mock(return_value=httpx.Response(200, text=html))

    # scrape_url is a StructuredTool, so we must use ainvoke
    text = await scrape_url.ainvoke(url)
    assert "alert(1)" not in text
    assert "Hello World" in text


@pytest.mark.asyncio  # type: ignore
@respx.mock  # type: ignore
async def test_scrape_url_redirect() -> None:
    url = "https://example.com/old"
    new_url = "https://example.com/new"
    respx.get(url).mock(return_value=httpx.Response(301, headers={"Location": new_url}))
    respx.get(new_url).mock(return_value=httpx.Response(200, text="<html><body>New Content</body></html>"))

    # scrape_url is a StructuredTool, so we must use ainvoke
    text = await scrape_url.ainvoke(url)
    assert "New Content" in text


@pytest.mark.asyncio  # type: ignore
@respx.mock  # type: ignore
async def test_scrape_url_empty_html() -> None:
    url = "https://example.com/empty"
    respx.get(url).mock(return_value=httpx.Response(200, text="<html></html>"))

    # scrape_url is a StructuredTool, so we must use ainvoke
    text = await scrape_url.ainvoke(url)
    assert text == ""


@pytest.mark.asyncio  # type: ignore
@respx.mock  # type: ignore
async def test_scrape_url_retry() -> None:
    url = "https://example.com/retry"
    # Fail once with connection error, then succeed
    route = respx.get(url)
    route.side_effect = [
        httpx.ConnectError("Fail 1"),
        httpx.Response(200, text="Success"),
    ]

    # scrape_url is a StructuredTool, so we must use ainvoke
    text = await scrape_url.ainvoke(url)
    assert text == "Success"
    assert route.call_count == 2
