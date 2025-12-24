# Technology Stack

## Core Architecture
- **Runtime:** Python 3.12+
- **Orchestration:** **LangGraph** (Stateful, cyclic multi-agent workflows)
- **Framework:** **LangChain** (Components & Interfaces)
- **Type Safety:** Pydantic (Strict data validation)

## Data & Memory
- **Vector Database:** **ChromaDB** (Local persistent storage)
- **Embeddings:** **OpenAI text-embedding-3-small**
- **LLM:** **gpt-5.2** (Reasoning & Synthesis)

## External Tools
- **Search:** **Tavily API** (Optimized for AI agents)
- **Scraping:** BeautifulSoup4 (for targeted extraction)

## Interface
- **API:** **FastAPI** (Production backend)
- **CLI:** **Typer** (Development testing)

## Design Principles
- **Agentic First:** Prefer graph-based state machines over linear chains.
- **Async Native:** All I/O operations must be asynchronous.
- **Modular:** Clear separation between `graph/`, `tools/`, and `domain/`.