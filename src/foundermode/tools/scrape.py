import httpx
from bs4 import BeautifulSoup


async def scrape_url(url: str) -> str:
    """Scrapes text content from a given URL asynchronously."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            soup = BeautifulSoup(response.text, "html.parser")

            # Basic content extraction: Remove script and style tags
            for script_or_style in soup(["script", "style"]):
                script_or_style.decompose()  # Remove tags

            # Get text, strip leading/trailing whitespace, and normalize spaces
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (line for line in lines if line)  # Filter out blank lines
            return "\n".join(chunks)

    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return ""
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ""
