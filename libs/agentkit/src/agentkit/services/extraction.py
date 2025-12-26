import logging

import httpx

from agentkit.infra.decorators import logged, with_fallback, with_retry

logger = logging.getLogger("agentkit.services.extraction")


class ExtractionService:
    """Service for extracting clean text content from URLs."""

    @logged()
    @with_fallback(fallback="Error: Could not extract content.")
    async def extract(self, url: str, use_playwright: bool = False) -> str:
        """
        Extract clean text from a URL using cascading logic.
        1. Playwright (optional/fallback)
        2. HTTP (httpx)
        3. Readability + BS4 cleaning
        """
        html = ""
        if use_playwright:
            html = await self._scrape_with_playwright(url)

        if not html:
            html = await self._fetch_html(url)

        if not html:
            return "Failed to retrieve HTML."

        return await self._clean_html(html)

    @with_retry(max_attempts=2)
    async def _fetch_html(self, url: str) -> str:
        """Fetch raw HTML using httpx."""
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            return str(response.text)

    async def _scrape_with_playwright(self, url: str) -> str:
        """Scrape URL using Playwright (Lazy Import)."""
        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, wait_until="networkidle", timeout=30000)
                content = await page.content()
                await browser.close()
                return str(content)
        except ImportError:
            logger.warning("Playwright not installed, skipping.")
            return ""
        except Exception as e:
            logger.error(f"Playwright scraping failed: {e}")
            return ""

    async def _clean_html(self, html: str) -> str:
        """Clean HTML using Readability and BS4 (Lazy Imports)."""
        try:
            from bs4 import BeautifulSoup
            from readability import Document

            doc = Document(html)
            summary_html = doc.summary()

            soup = BeautifulSoup(summary_html, "html.parser")
            text = soup.get_text()

            # Fallback to full BS4 if readability result is too sparse
            if len(text.strip()) < 500:
                full_soup = BeautifulSoup(html, "html.parser")
                for s in full_soup(["script", "style"]):
                    s.decompose()
                text = full_soup.get_text()

            lines = (line.strip() for line in text.splitlines())
            return "\n".join(chunk for chunk in lines if chunk)

        except ImportError as e:
            logger.error(f"Cleaning libraries not installed: {e}")
            return "Error: Missing cleaning dependencies (readability-lxml, beautifulsoup4)."
        except Exception as e:
            logger.error(f"HTML cleaning failed: {e}")
            return "Error: Failed to clean HTML."
