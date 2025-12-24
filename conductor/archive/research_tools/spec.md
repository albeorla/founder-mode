# Specification: The Research Tools

## Context
The FounderMode agent needs "hands" to interact with the world. This track focuses on implementing the core research tools: a web search tool (Tavily) and a web scraper (BeautifulSoup). These tools will allow the agent to gather real-world data to validate business ideas.

## Requirements

### 1. Tavily Search Tool (`tools/search.py`)
- Wrap the Tavily API into a LangChain-compatible `BaseTool`.
- Requirements:
    - Input: A search query string.
    - Output: A list of results, each containing `title`, `url`, `snippet`, and ideally full `content`.
    - Handle API keys via environment variables (`TAVILY_API_KEY`).
    - Implement error handling for API failures.

### 2. Web Scraper (`tools/scrape.py`)
- Build a utility to extract clean text from a given URL.
- Requirements:
    - Use `BeautifulSoup4` for parsing.
    - Use `httpx` for asynchronous HTTP requests.
    - Extract main content text while filtering out boilerplate (nav, footer, ads).
    - Handle common issues like timeouts and 404s.

### 3. Research Task Logic
- Refine the domain logic for handling research tasks.
- Requirements:
    - Ability to convert a high-level question into a specific search or scrape action.
    - Structuring the output so it can be ingested by the memory system (in the next track).

## Acceptance Criteria
- [ ] `TavilySearch` tool successfully returns results for a test query.
- [ ] `WebScraper` successfully extracts readable text from a known URL (e.g., a news article).
- [ ] Tools are integrated into the project's dependency management (`uv`).
- [ ] Comprehensive unit tests for both tools, including mocking of network requests.
