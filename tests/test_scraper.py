import httpx
import pytest
import respx

from foundermode.tools.scrape import scrape_url


@pytest.mark.asyncio  # type: ignore
@respx.mock  # type: ignore
async def test_scrape_url_success() -> None:
    url = "https://example.com"
    respx.get(url).mock(return_value=httpx.Response(200, text="<html><body><h1>Hello World</h1></body></html>"))

    text = await scrape_url(url)
    assert "Hello World" in text


@pytest.mark.asyncio  # type: ignore
@respx.mock  # type: ignore
async def test_scrape_url_failure() -> None:
    url = "https://example.com/notfound"
    respx.get(url).mock(return_value=httpx.Response(404))

    text = await scrape_url(url)
    assert text == ""


@pytest.mark.asyncio  # type: ignore
@respx.mock  # type: ignore
async def test_scrape_url_strips_scripts() -> None:
    url = "https://example.com/js"
    html = "<html><body><script>alert(1)</script><h1>Hello World</h1></body></html>"
    respx.get(url).mock(return_value=httpx.Response(200, text=html))

    text = await scrape_url(url)
    assert "alert(1)" not in text
    assert "Hello World" in text


@pytest.mark.asyncio  # type: ignore
@respx.mock  # type: ignore
async def test_scrape_url_redirect() -> None:
    url = "https://example.com/old"
    new_url = "https://example.com/new"
    respx.get(url).mock(return_value=httpx.Response(301, headers={"Location": new_url}))
    respx.get(new_url).mock(return_value=httpx.Response(200, text="<html><body>New Content</body></html>"))

    text = await scrape_url(url)
    assert "New Content" in text


@pytest.mark.asyncio  # type: ignore
@respx.mock  # type: ignore
async def test_scrape_url_empty_html() -> None:
    url = "https://example.com/empty"
    respx.get(url).mock(return_value=httpx.Response(200, text="<html></html>"))

    text = await scrape_url(url)
    assert text == ""


@pytest.mark.asyncio  # type: ignore
@respx.mock  # type: ignore
async def test_scrape_url_retry() -> None:
    url = "https://example.com/retry"
    # Fail twice with connection error, then succeed
    route = respx.get(url)
    route.side_effect = [
        httpx.ConnectError("Fail 1"),
        httpx.ConnectError("Fail 2"),
        httpx.Response(200, text="Success"),
    ]

    text = await scrape_url(url)
    assert text == "Success"
    assert route.call_count == 3
