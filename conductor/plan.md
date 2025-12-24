# Project Plan: FounderMode

## Phase 1: Foundation & Memory Systems
- [ ] Task: Initialize project structure.
    - Set up `pyproject.toml` with `langgraph`, `langchain`, `chromadb`, `fastapi`, `pydantic`.
    - Create directory structure: `src/foundermode/{domain,graph,memory,tools,api}`.
- [ ] Task: Implement Domain Models (`domain/schema.py`).
    - Define `Idea`, `ResearchTask`, and `MarketReport` Pydantic models.
- [ ] Task: Implement Vector Store (`memory/vector_store.py`).
    - Create `ChromaManager` class for adding/querying text embeddings.
    - **Verification:** Write a script that ingests 5 mock facts and retrieves the most semantically similar one.

## Phase 2: The Research Tools
- [ ] Task: Implement Search Tool (`tools/search.py`).
    - Wrap Tavily API into a LangChain `Tool`.
- [ ] Task: Implement Scraper Tool (`tools/scrape.py`).
    - Build a basic URL-to-Markdown fetcher.

## Phase 3: The Agent Graph
- [ ] Task: Define Graph State (`domain/state.py`).
- [ ] Task: Build the Analyst Node (`graph/nodes/analyst.py`).
- [ ] Task: Build the Researcher Node (`graph/nodes/researcher.py`).
- [ ] Task: Wire the LangGraph workflow (`graph/workflow.py`).
    - **Verification:** Run a flow that takes a query -> researches it -> summarizes it.