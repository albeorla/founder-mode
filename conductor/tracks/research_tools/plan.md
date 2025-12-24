# Plan: The Research Tools

## Phase 1: Search Integration
- [x] Task: Implement Tavily Search Tool 6b73141
    - Create `src/foundermode/tools/search.py`.
    - Implement the `TavilySearch` class inheriting from LangChain's `BaseTool`.
- [ ] Task: Verify Search Tool
    - Write `tests/test_search_tool.py` with mocks for the Tavily API.

## Phase 2: Web Scraping
- [ ] Task: Implement Web Scraper
    - Create `src/foundermode/tools/scrape.py`.
    - Build an async scraper using `httpx` and `BeautifulSoup`.
- [ ] Task: Verify Scraper
    - Write `tests/test_scraper.py` with mocks for HTTP requests.

## Phase 3: Integration & Logic
- [ ] Task: Refine Research Logic
    - Update `src/foundermode/domain/schema.py` if needed to better support tool outputs.
- [ ] Task: Final Verification
    - Execute the Phase Completion Verification and Checkpointing Protocol.
