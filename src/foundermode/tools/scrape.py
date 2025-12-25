import logging
from typing import Any

import httpx
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from readability import Document
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class ScraperResult:
    """Container for scraper results."""

    def __init__(self, content: str, metadata: dict[str, Any], status: str):
        self.content = content
        self.metadata = metadata
        self.status = status


async def scrape_with_readability(html: str) -> str:
    """Extracts main content using Readability-lxml."""
    doc = Document(html)
    return str(doc.summary())


async def scrape_with_bs4(html: str) -> str:
    """Extracts text content using BeautifulSoup4 as a fallback or for metadata."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove script and style tags
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    # Get text
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (line for line in lines if line)
    return "\n".join(chunks)


@retry(  # type: ignore
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=1, min=2, max=5),
)
async def fetch_html(url: str) -> str:
    """Fetches raw HTML from a URL."""
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        response = await client.get(url)
        response.raise_for_status()
        return str(response.text)


async def scrape_with_playwright(url: str) -> str:
    """
    Scrapes a URL using Playwright for dynamic content.
    Note: Requires playwright to be installed and initialized.
    """
    try:
        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, wait_until="networkidle", timeout=30000)
            content = await page.content()
            await browser.close()
            return str(content)
    except Exception as e:
        logger.error(f"Playwright scraping failed for {url}: {e}")
        return ""


@tool  # type: ignore
async def deep_scrape_url(url: str, use_playwright: bool = False) -> str:
    """
    Advanced scraper that extracts clean text from a URL using multi-stage logic.
    Supports dynamic rendering via Playwright if specified.
    """
    logger.info(f"Deep scraping URL: {url} (Playwright: {use_playwright})")

    html = ""
    try:
        if use_playwright:
            try:
                html = await scrape_with_playwright(url)
            except Exception as e:
                logger.warning(f"Playwright execution failed, falling back: {e}")
                html = ""

        if not html:
            html = await fetch_html(url)

        if not html:
            return "Failed to retrieve content."

        # Stage 1: Readability
        clean_html = await scrape_with_readability(html)
        # Convert summary HTML to text
        summary_soup = BeautifulSoup(clean_html, "html.parser")
        text_content = summary_soup.get_text()

        # Stage 2: Fallback to full BS4 if readability is too short
        if len(text_content) < 500:
            logger.info("Readability content too short, falling back to BS4.")
            text_content = await scrape_with_bs4(html)

        return str(text_content)

    except Exception as e:
        logger.error(f"Deep scraping failed for {url}: {e}")
        return f"Error scraping {url}: {str(e)}"


# Maintain backward compatibility for now
@tool  # type: ignore
async def scrape_url(url: str) -> str:
    """Scrapes text content from a given URL asynchronously."""
    return str(await deep_scrape_url(url))
