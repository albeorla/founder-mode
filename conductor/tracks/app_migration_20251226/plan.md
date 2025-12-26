# Project Plan - Phase 1: First App Migration

This plan covers the migration of `founder-mode` to the `apps/` directory and its integration with `libs/agentkit`.

## Phase 1: Structure & Configuration
Goal: Set up the monorepo workspace and directories.

- [ ] **Task: Create directory structure**
  - Create `apps/founder-mode` and `apps/founder-mode/src`.
  - Ensure `.gitkeep` or initial structure is in place.
- [ ] **Task: Configure uv workspaces**
  - Update root `pyproject.toml` to include:
    ```toml
    [tool.uv]
    workspaces = ["libs/*", "apps/*"]
    ```
- [ ] **Task: Create app-specific pyproject.toml**
  - Initialize `apps/founder-mode/pyproject.toml` with basic metadata and dependency on `agentkit`.
- [ ] Task: Conductor - User Manual Verification 'Structure & Configuration' (Protocol in workflow.md)

## Phase 2: Code Migration
Goal: Move the existing logic to its new home.

- [ ] **Task: Move source code**
  - Move `src/foundermode` to `apps/founder-mode/src/foundermode`.
- [ ] **Task: Update imports**
  - Fix any relative or absolute imports within `apps/founder-mode` that broke during the move.
- [ ] **Task: Move tests**
  - Move `tests/` content relevant to `founder-mode` to `apps/founder-mode/tests/`.
- [ ] Task: Conductor - User Manual Verification 'Code Migration' (Protocol in workflow.md)

## Phase 3: Agentkit Integration
Goal: Replace redundant app code with library calls.

- [ ] **Task: Refactor LLM service**
  - Replace `apps/founder-mode/src/foundermode/services/llm.py` logic with `agentkit.services.llm`.
- [ ] **Task: Refactor Search service**
  - Replace `apps/founder-mode/src/foundermode/services/search.py` logic with `agentkit.services.search`.
- [ ] **Task: Refactor Vector Store service**
  - Replace `apps/founder-mode/src/foundermode/services/vector_store.py` logic with `agentkit.services.vector_store`.
- [ ] Task: Conductor - User Manual Verification 'Agentkit Integration' (Protocol in workflow.md)

## Phase 4: Final Verification & Cleanup
Goal: Ensure everything works and remove the old monolith structure.

- [ ] **Task: Run all tests**
  - Execute `uv run pytest` from the root to verify both `agentkit` and `founder-mode`.
- [ ] **Task: Docker build check**
  - Update `Dockerfile` to support the new monorepo structure and ensure it builds.
- [ ] **Task: Cleanup**
  - Remove the old `src/` directory at the root.
- [ ] Task: Conductor - User Manual Verification 'Final Verification & Cleanup' (Protocol in workflow.md)
