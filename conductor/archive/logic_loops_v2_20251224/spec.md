# Specification: logic_loops_v2

## Overview
This track focuses on transitioning the FounderMode system from a "Walking Skeleton" with mock data to a functional "Senior-level Agentic System." This involves implementing real logic for the Planner, Researcher, and Writer agents, integrating them into a cyclic graph, establishing a robust "Working Memory" using ChromaDB, and ensuring a clean development workflow.

## Functional Requirements

### 1. Configuration Management
- Implement a `Settings` class using `pydantic-settings`.
- Load configuration from environment variables and a `.env` file.
- Support validation for `OPENAI_API_KEY` and `TAVILY_API_KEY`.

### 2. Dynamic Node Logic & Graph Wiring
- Update `src/foundermode/graph/workflow.py` to orchestrate the `Planner`, `Researcher`, and `Writer` nodes.
- **Dynamic Fallback:** Nodes must attempt to use live LLM logic (GPT-4o) but automatically fallback to `Mock` logic if necessary API keys are missing or invalid.

### 3. Integrated Working Memory
- Update `src/foundermode/tools/search.py` to integrate with `src/foundermode/memory/vector_store.py`.
- **Search-as-Memory:** Before calling the external Tavily API, the system should query local ChromaDB for existing relevant context.
- **Automatic Upsert:** New search results must be automatically embedded and stored in ChromaDB.
- **Metadata & Deduplication:** Tag results with source URLs/queries and implement similarity-based deduplication before storage.

### 4. Workflow & Cleanup
- **Directory Hygiene:** Create an `.out/` directory for all generated artifacts (reports, memos) and ensure it is added to `.gitignore`.
- **Cleanup:** Move or remove existing root-level HTML reports (`test_memo.html`, etc.) into `.out/`.
- **Branch-Based Workflow:** Strictly adhere to a branch-based implementation for every task (e.g., `task/feature-name`).

## Non-Functional Requirements
- **Async Native:** All network and database I/O must remain asynchronous.
- **Type Safety:** Maintain strict Pydantic model usage for graph state and tool inputs.

## Acceptance Criteria
- [ ] The system can successfully run a full research cycle using live APIs when keys are provided.
- [ ] The system falls back to mock responses gracefully if keys are missing.
- [ ] Search results are verifiably stored in the local `ChromaDB` instance.
- [ ] API keys are managed centrally via the `Settings` object.
- [ ] No HTML artifacts are present in the project root; all are in `.out/` (and ignored by git).
- [ ] All implementation tasks are completed on dedicated feature branches.

## Out of Scope
- Implementation of the HTML Report generation (Writer logic will focus on Markdown/Text synthesis for now).
- Deployment to cloud environments.
