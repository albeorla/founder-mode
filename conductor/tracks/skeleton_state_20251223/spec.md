# Specification: The Skeleton & State

## Context
This is the "Walking Skeleton" track. We are building the minimal end-to-end infrastructure for the FounderMode agent. We will not implement real AI logic yet, but we will establish the state schema, the graph architecture, and the CLI entry point.

## Requirements

### 1. Project Structure
- Ensure directories exist: `src/foundermode/{domain,graph,memory,tools,api}`.
- Ensure dependencies are installed: `langgraph`, `fastapi`, `pydantic`, `typer` (CLI), `langsmith` (for tracing).

### 2. Domain Models (`domain/schema.py`)
- **`ResearchPlan`**: A list of questions/tasks.
- **`ResearchFact`**: A single verified piece of information (source, content).
- **`InvestmentMemo`**: The final output structure (executive summary, market, competitors).

### 3. Graph State (`domain/state.py`)
- **`GraphState`**: A TypedDict containing:
    - `query`: str (User input)
    - `plan`: ResearchPlan
    - `facts`: List[ResearchFact]
    - `draft`: InvestmentMemo
    - `messages`: List[BaseMessage] (LangChain history)

### 4. Mock Nodes (`graph/nodes/mock.py`)
- **`MockAnalyst`**: A function that accepts `GraphState` and returns a state update with a hardcoded `ResearchPlan` and dummy `InvestmentMemo`, simulating work.

### 5. Workflow (`graph/workflow.py`)
- A simple linear graph: `START` -> `MockAnalyst` -> `END`.
- Must be compiled into a `CompiledGraph`.

### 6. CLI (`api/cli.py`)
- A Typer app.
- Command: `foundermode run <query>`.
- Behavior: Invokes the graph, streams events (if possible), and prints the final `draft`.

## Acceptance Criteria
- [ ] `uv run foundermode run "Test Idea"` executes successfully.
- [ ] Output contains "Mock Executive Summary".
- [ ] LangSmith trace is visible (if env vars provided).
- [ ] Code passes `ruff` and `mypy`.
