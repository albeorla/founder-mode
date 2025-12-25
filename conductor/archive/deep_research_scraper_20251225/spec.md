# Track Spec: deep_research_scraper_20251225

## Overview
This track upgrades the FounderMode Researcher from a "Snippet-Only" agent to a deep prowler that reads and understands full web pages. It addresses the "Empty Hands" problem identified in V2 by providing the Critic Node with the specific quantitative data (pricing, features, metrics) it demands.

## Functional Requirements
- **Unified Scraper Tool (`scrape.py`):**
    - Implementation of a robust scraper using a multi-stage approach:
        - `Readability-lxml` for clean text extraction.
        - `BeautifulSoup4` for targeted HTML parsing (metadata, headers).
        - `Playwright` integration for rendering JavaScript-heavy pages (SPAs).
- **Autonomous Selector (`researcher.py`):**
    - Update the Researcher node to analyze search results via LLM and select 1-3 high-signal URLs for "Deep Diving."
- **Hybrid Data Processing:**
    - **Extraction (State):** For every scraped page, extract a structured "Data Sheet" (prices, key features, dates) to return to the Planner immediately.
    - **Ingestion (Memory):** Implement semantic chunking to store the full text in ChromaDB, ensuring the Writer can cite specific evidence.
- **Robust Error Handling:** Detect and handle "Bot Detection" or failures gracefully by falling back to search snippets with a warning log.

## Evaluation & Success Criteria
- **Data Density:** Verify that memos generated using the Scraper contain quantitative pricing or feature details that were absent in search snippets.
- **Citation Verification:** Use LangSmith to confirm the Writer is retrieving and citing content from the scraped full-text chunks in ChromaDB.
- **Robustness:** 100% success rate in extracting text from top-tier competitor pages (e.g., Salesforce, Stripe, Shopify pricing pages).

## Out of Scope
- Scraping pages behind authentication/logins.
- Automated CAPTCHA solving.
