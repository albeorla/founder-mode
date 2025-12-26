# Technology Stack

## Monorepo Architecture

```
founder-mode/
├── libs/agentkit/       # Shared toolkit (standardized)
├── apps/*/              # Individual apps (domain-specific)
└── infra/               # CI/CD, Docker, scripts
```

### agentkit (Shared Library)

| Module | Purpose |
|--------|---------|
| `infra/config` | Settings + environment-based overrides |
| `infra/logging` | Structured logging with context |
| `infra/decorators` | `@logged`, `@with_fallback`, `@retry` |
| `services/llm` | `create_llm()` factory for model instantiation |
| `services/search` | Tavily wrapper with rate limiting |
| `services/extraction` | Cascading scraper (Playwright → Readability → BS4) |
| `services/vector_store` | ChromaDB + InMemory backends |
| `testing/fixtures` | Pytest fixtures for mocking external services |
| `patterns/` | Copy-paste LangGraph workflow templates |

### Apps (Domain-Specific)

Each app contains only:
- `nodes/` — LangGraph node functions
- `prompts/` — Domain-specific prompts
- `schemas/` — Pydantic models
- `workflow.py` — Graph definition
- `cli.py` — Entry point

---

## Core Technologies

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Runtime** | Python 3.12+ | Modern async, type hints |
| **Orchestration** | LangGraph | Stateful, cyclic multi-agent workflows |
| **Framework** | LangChain | Components & interfaces |
| **Type Safety** | Pydantic, pydantic-settings | Strict data & config validation |
| **Observability** | LangSmith | Tracing & debugging |

## Data & Memory

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Vector DB** | ChromaDB | Local persistent storage |
| **Embeddings** | OpenAI text-embedding-3-small | Semantic similarity |
| **LLM** | gpt-4o | Reasoning & synthesis |

## External Services

| Service | Technology | Purpose |
|---------|------------|---------|
| **Search** | Tavily API | AI-optimized web search |
| **Scraping** | Playwright | Dynamic JS rendering |
| **Fallback** | Readability-lxml, BeautifulSoup4 | Clean text extraction |

## Interface

| Layer | Technology | Purpose |
|-------|------------|---------|
| **API** | FastAPI + uvicorn | Production backend |
| **CLI** | Typer | Development & testing |

## Development & Build

| Tool | Purpose |
|------|---------|
| **uv** | High-speed dependency management |
| **Hatchling** | Standards-based packaging |
| **Ruff** | Fast unified linter/formatter |
| **Mypy** | Strict static type analysis |
| **Pytest** | Testing framework |

## Evaluation & Testing

| Tool | Purpose |
|------|---------|
| **LangSmith Datasets** | Benchmark datasets |
| **LLM-as-a-Judge** | Custom rubric evaluators |
| **pytest-xdist** | Parallel test execution |
| **pytest-testmon** | Incremental test selection |

---

## Design Principles

### Toolkit, Not Framework
- Decorators over base classes
- LangGraph directly, no wrappers
- Document patterns, don't encode them

### Lazy Everything
- Lazy imports for heavy deps (Playwright, ChromaDB)
- Lazy config loading
- Lazy service initialization

### Agentic First
- Graph-based state machines over linear chains
- Cyclic workflows with self-correction
- Human-in-the-loop approval gates

### Async Native
- All I/O operations must be asynchronous
- Connection pooling for external services

### Dynamic Fallback
- Handle missing API keys gracefully
- Mock data for local development and CI
- Cascading extraction (Playwright → Readability → BS4)
