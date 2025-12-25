# Technology Stack

## Core Architecture
- **Runtime:** Python 3.12+
- **Orchestration:** **LangGraph** (Stateful, cyclic multi-agent workflows)
- **Framework:** **LangChain** (Components & Interfaces)
- **Type Safety:** Pydantic and **pydantic-settings** (Strict data & config validation)
- **Observability:** **LangSmith** (Tracing & Debugging)

## Evaluation & Testing
- **Benchmarking:** **LangSmith Datasets**
- **Quality Control:** **LLM-as-a-Judge** (Custom rubric evaluators)
- **Testing Framework:** **Pytest**

## Data & Memory
- **Vector Database:** **ChromaDB** (Local persistent storage)
- **Embeddings:** **OpenAI text-embedding-3-small**
- **LLM:** **gpt-4o** (Reasoning & Synthesis)

## External Tools
- **Search:** **Tavily API** (Optimized for AI agents)
- **Scraping:** **Playwright** (Dynamic rendering), **Readability-lxml** (Clean text extraction), and **BeautifulSoup4** (Targeted parsing)

## Interface
- **API:** **FastAPI** with **uvicorn** (Production backend)
- **CLI:** **Typer** (Development testing)

## Development & Build
- **Package Manager:** **uv** (High-speed dependency management)
- **Build Backend:** **Hatchling** (Standards-based packaging)
- **Linting & Formatting:** **Ruff** (Fast, unified linter/formatter)
- **Type Checking:** **Mypy** (Strict mode static analysis)
- **Testing:** **Pytest**

## Design Principles
- **Agentic First:** Prefer graph-based state machines over linear chains.
- **Async Native:** All I/O operations must be asynchronous.
- **Modular:** Clear separation between `graph/`, `tools/`, and `domain/`.
- **Dynamic Fallback:** Systems must handle missing API keys gracefully with mock data for local development and CI.
