# Plan: Interface & Polish

## Phase 1: Human-in-the-Loop (CLI)
- [x] Task: Configure Graph Checkpointing
    - Update `src/foundermode/graph/workflow.py` to use `MemorySaver` (or SQLite) and set `interrupt_before=["researcher"]`.
- [x] Task: Update CLI for Interaction
    - Update `src/foundermode/api/cli.py` to handle the pause.
    - Display the generated plan.
    - Prompt user: "Approve or Edit?".
    - Resume graph execution with updated state if edited.

## Phase 2: Report Generation
- [ ] Task: Implement HTML Renderer
    - Create `src/foundermode/tools/reporter.py`.
    - Function: `render_memo(memo: InvestmentMemo, filename: str) -> str`.
    - Use a simple Jinja2 template or string replacement with basic CSS.
- [ ] Task: Integrate Renderer into Workflow
    - Update `src/foundermode/graph/workflow.py` (or a new `Publisher` node) to save the report at the end of the run.

## Phase 3: The API
- [ ] Task: Setup FastAPI Skeleton
    - Create `src/foundermode/api/server.py`.
    - Define request/response models.
- [ ] Task: Implement Run & Status Endpoints
    - `POST /run`: Trigger the background graph execution.
    - `GET /run/{id}`: Poll for status.
- [ ] Task: Implement Resume Endpoint
    - `POST /run/{id}/resume`: Handle the HITL approval via API.
