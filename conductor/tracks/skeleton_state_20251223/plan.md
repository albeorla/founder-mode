# Plan: The Skeleton & State

## Phase 1: Structure & Schema [checkpoint: ef42124]
- [x] Task: Project Structure & Dependencies 8130fea
    - Create folders: `src/foundermode/{domain,graph,memory,tools,api}`.
    - Add dependencies: `langgraph`, `langchain-core`, `typer`, `langsmith`.
- [x] Task: Define Domain Models 7aafca8
    - Implement `src/foundermode/domain/schema.py` with Pydantic models.
- [x] Task: Define Graph State 697cd0b
    - Implement `src/foundermode/domain/state.py` with `GraphState`.

## Phase 2: Graph Logic (Mock) [checkpoint: 3f29280]
- [x] Task: Implement Mock Analyst c63eb54
    - Create `src/foundermode/graph/nodes/mock.py`.
- [x] Task: Wire Workflow 12b5373
    - Create `src/foundermode/graph/workflow.py` with `StateGraph`.

## Phase 3: Interface & Verification
- [ ] Task: Implement CLI
    - Create `src/foundermode/api/cli.py` using Typer.
    - Register command in `pyproject.toml` (`[project.scripts]`).
- [ ] Task: Final Verification
    - Run the CLI end-to-end.
