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
