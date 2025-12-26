# Track Spec: Phase 1: First App Migration

## Overview
This track focuses on migrating the existing `founder-mode` application into the new monorepo structure as `apps/founder-mode`. Additionally, the application will be refactored to consume common services from the newly created `libs/agentkit`.

## Objectives
- Establish the `apps/` directory and move `founder-mode` source code.
- Update the project configuration (`pyproject.toml`) to reflect the monorepo structure and dependencies.
- Integrate `libs/agentkit` into `apps/founder-mode`, replacing redundant implementations of LLM, search, and vector store services.
- Ensure all tests pass in the new structure.

## Scope
- **apps/founder-mode**: New location for the application.
- **src/foundermode**: Source to be moved.
- **libs/agentkit**: Library to be integrated.
- **pyproject.toml**: Root configuration update.

## Technical Details
- **Structure**: `apps/founder-mode` will have its own `src/` directory and `pyproject.toml` (if necessary, or handled via root monorepo config).
- **Dependencies**: `apps/founder-mode` will depend on `libs/agentkit`.
- **Refactoring**: Replace `src/foundermode/services` with imports from `agentkit.services`.

## Success Criteria
- `apps/founder-mode` exists and contains the migrated source code.
- Application runs using `libs/agentkit` services.
- All integration and e2e tests pass.
- `uv run pytest` executed from the root correctly runs tests for both the library and the app.
