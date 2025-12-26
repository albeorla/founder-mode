# Implementation Plan: agentkit_library_build_20251225

## Phase 1: Scaffolding & Infrastructure
- [x] Create `libs/agentkit/` directory structure + `pyproject.toml`
- [x] Implement `agentkit.infra.config` (pydantic-settings, .env, test overrides)
- [x] Implement `agentkit.infra.logging` (structured JSON + colored console)
- [x] Implement `agentkit.infra.decorators` ( @logged, @with_fallback, @with_retry, @with_timeout)
- [x] Create `__init__.py` with public API exports
- [x] Manual Verification: Scaffolding & Infrastructure

## Phase 2: Core Services
- [x] Port `agentkit.services.llm` (create_llm factory)
- [ ] Port `agentkit.services.search` (Tavily wrapper)
- [x] Port `agentkit.services.extraction` (cascading scraper, lazy imports)
- [x] Port `agentkit.services.vector_store` (ChromaDB + InMemory, lazy imports)
- [x] Manual Verification: Core Services

## Phase 3: Testing & Verification
- [x] Implement `agentkit.testing.fixtures` (mock_settings, mock_llm, mock_search, mock_vector_store)
- [ ] Create example `conftest.py` showing fixture usage
- [x] Write unit tests for decorators and services
- [x] Verify lazy loading (import without Playwright/ChromaDB installed)
- [x] Manual Verification: Testing & Verification

## Phase 4: Documentation & Patterns
- [x] Create `patterns/WORKFLOWS.md` with LangGraph examples
- [x] Manual Verification: Documentation & Patterns

## Deferred (add when needed)
- [ ] `agentkit.services.council` (OpenRouter multi-model)
- [ ] `agentkit.testing.fixtures.mock_council_service`
