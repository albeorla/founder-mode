# Specification: agentkit_library_build_20251225

## Overview
Build `libs/agentkit` as a functional toolkit for LangGraph agents. Architecture: decorators + dependency injection, no inheritance hierarchies.

## Structure
```
libs/agentkit/
├── infra/           # Config, logging, decorators
├── services/        # LLM, search, extraction, vector store, council
├── testing/         # Pytest fixtures
└── patterns/        # Documented workflow patterns
```

## Functional Requirements

### 1. Infrastructure (`agentkit.infra`)
- **config.py**: Lazy singleton via `pydantic-settings`, `.env` loading, test override support
- **logging.py**: Structured logging (JSON prod, readable dev), `setup_logging()` utility
- **decorators.py**: `@logged`, `@with_fallback`, `@with_retry`, `@with_timeout` — all support sync + async

### 2. Core Services (`agentkit.services`)
Port from `src/foundermode/`, refactor for DI:
- **llm.py**: `create_llm()` factory, auto-detect provider from model name
- **search.py**: Tavily wrapper with graceful degradation
- **extraction.py**: Cascading scraper (Playwright → HTTP → Readability → BS4)
- **vector_store.py**: ChromaDB wrapper + `InMemoryVectorStore` for tests
- **council.py** (optional): OpenRouter parallel queries for multi-model consensus

### 3. Testing Utilities (`agentkit.testing`)
- **fixtures.py**: `mock_settings`, `mock_llm`, `mock_search`, `mock_vector_store`, `mock_council_service`

### 4. Patterns Documentation (`agentkit/patterns`)
- **WORKFLOWS.md**: Copy-paste LangGraph patterns (linear, loop, HITL, parallel)
- **council.py**: Multi-model consensus workflow (collect → review → synthesize)

## Non-Functional Requirements
- No base classes or inheritance
- Services accept explicit config, default to `get_settings()`
- Lazy imports for heavy deps (Playwright, ChromaDB)

## Acceptance Criteria
- [ ] `libs/agentkit/` scaffolded with all modules
- [ ] Decorators work with `def` and `async def`
- [ ] Services pass unit tests using `agentkit.testing` mocks
- [ ] Library importable without Playwright/ChromaDB installed (lazy loading)
- [ ] Lives at `libs/agentkit/` in existing repo (no workspace extraction yet)

## Out of Scope
- Migration of `founder-mode` app logic (separate track)
- `uv workspace` configuration
- Evaluators (add when needed in app)
