# Plan: The Skeleton & State

## Phase 1: Structure & Schema
- [~] Task: Project Structure & Dependencies
    - Create folders: `src/foundermode/{domain,graph,memory,tools,api}`.
    - Add dependencies: `langgraph`, `langchain-core`, `typer`, `langsmith`.
- [ ] Task: Define Domain Models
    - Implement `src/foundermode/domain/schema.py` with Pydantic models.
- [ ] Task: Define Graph State
    - Implement `src/foundermode/domain/state.py` with `GraphState`.

## Phase 2: Graph Logic (Mock)
- [ ] Task: Implement Mock Analyst
    - Create `src/foundermode/graph/nodes/mock.py`.
- [ ] Task: Wire Workflow
    - Create `src/foundermode/graph/workflow.py` with `StateGraph`.

## Phase 3: Interface & Verification
- [ ] Task: Implement CLI
    - Create `src/foundermode/api/cli.py` using Typer.
    - Register command in `pyproject.toml` (`[project.scripts]`).
- [ ] Task: Final Verification
    - Run the CLI end-to-end.
