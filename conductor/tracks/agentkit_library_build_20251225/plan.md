# Implementation Plan: agentkit_library_build_20251225

## Phase 1: Scaffolding & Infrastructure
- [ ] Create `libs/agentkit/` directory structure + `pyproject.toml`
- [ ] Implement `agentkit.infra.config` (pydantic-settings, .env, test overrides)
- [ ] Implement `agentkit.infra.logging` (structured JSON + colored console)
- [ ] Implement `agentkit.infra.decorators` ( @logged, @with_fallback, @with_retry, @with_timeout)
- [ ] Create `__init__.py` with public API exports
- [ ] Manual Verification: Scaffolding & Infrastructure

## Phase 2: Core Services
- [ ] Port `agentkit.services.llm` (create_llm factory)
- [ ] Port `agentkit.services.search` (Tavily wrapper)
- [ ] Port `agentkit.services.extraction` (cascading scraper, lazy imports)
- [ ] Port `agentkit.services.vector_store` (ChromaDB + InMemory, lazy imports)
- [ ] Manual Verification: Core Services

## Phase 3: Testing & Verification
- [ ] Implement `agentkit.testing.fixtures` (mock_settings, mock_llm, mock_search, mock_vector_store)
- [ ] Create example `conftest.py` showing fixture usage
- [ ] Write unit tests for decorators and services
- [ ] Verify lazy loading (import without Playwright/ChromaDB installed)
- [ ] Manual Verification: Testing & Verification

## Phase 4: Documentation & Patterns
- [ ] Create `patterns/WORKFLOWS.md` with LangGraph examples
- [ ] Manual Verification: Documentation & Patterns

## Deferred (add when needed)
- [ ] `agentkit.services.council` (OpenRouter multi-model)
- [ ] `agentkit.testing.fixtures.mock_council_service`
