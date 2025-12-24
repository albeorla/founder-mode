# Specification: Interface & Polish

## Context
The core logic of FounderMode (Planner -> Researcher -> Writer) is working. We now need to make it accessible and usable. This involves three key improvements:
1.  **Human-in-the-Loop (HITL):** Allowing the user to review and modify the "Research Plan" before execution.
2.  **Report Generation:** converting the raw Markdown output into a polished artifact (HTML/PDF).
3.  **API:** Exposing the workflow via a REST API (FastAPI) for external consumption (or a future UI).

## Goals
1.  Modify `graph/workflow.py` to support graph interruption.
2.  Update `api/cli.py` to support interactive feedback during the run.
3.  Create a `tools/reporter.py` module to render the Investment Memo.
4.  Implement `api/server.py` with FastAPI.

## Technical Requirements

### 1. Human-in-the-Loop
*   **Mechanism:** Use LangGraph's `checkpointer` and `interrupt_before` capabilities.
*   **Checkpoint:** Pause *after* the `Planner` node but *before* the `Researcher` node.
*   **Interaction:**
    *   The user sees the generated `ResearchPlan`.
    *   The user can approve it (continue) or edit it (update state -> continue).

### 2. Report Generation
*   **Format:** HTML (standalone file with basic CSS).
*   **Input:** The `InvestmentMemo` object (specifically the `content` field).
*   **Output:** `reports/{project_name}_memo.html`.
*   **Styling:** Clean, professional, minimal "Founder Mode" aesthetic.

### 3. FastAPI Server
*   **Framework:** `fastapi`, `uvicorn`.
*   **Endpoints:**
    *   `POST /run`: Accepts `{ "idea": "..." }`. Returns `{ "run_id": "..." }`.
    *   `GET /runs/{run_id}`: Returns current state/status.
    *   `POST /runs/{run_id}/resume`: Accepts modified state to resume a paused graph.
*   **Concurrency:** Must handle async graph execution (using `AsyncSqliteSaver` or similar simple checkpointer for now).

## Testing Strategy
*   **Unit Tests:** Test the report generator handles markdown correctly.
*   **Integration Tests:** Test the API endpoints using `TestClient`.
*   **Manual:** Verify the CLI interactive mode works as expected.
