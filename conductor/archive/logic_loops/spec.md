# Specification: The Logic Loops (LangGraph)

## Context
With the memory system (Vector Brain) and basic tools in place, we now need the "brain" of the agent. This track focuses on implementing the **LangGraph** workflow that orchestrates the due diligence process. The agent needs to cycle between planning, researching (using tools + memory), and writing/refining the investment memo.

## Requirements

### 1. State Definition (`domain/state.py`)
- Define the `FounderState` TypedDict/Pydantic model.
- **Keys:**
    - `research_question`: The original user prompt.
    - `research_facts`: List of collected `ResearchFact`s.
    - `memo_draft`: The current state of the `InvestmentMemo`.
    - `messages`: Chat history (LangChain `BaseMessage` list).
    - `next_step`: Indicator for the conditional edge (e.g., "research", "write", "finish").

### 2. Graph Nodes (`graph/nodes/`)
- **`planner`**: Analyzes the request and existing facts to decide the next immediate research task or if it's time to write.
- **`researcher`**:
    - Takes a query from the planner.
    - Uses `TavilySearch` to find info.
    - Uses `ChromaManager` (from previous track) to store valid facts.
    - *Crucial:* Deduplicates against existing memory before searching.
- **`writer`**:
    - Synthesizes the stored facts in `ChromaDB` into the specific sections of the `InvestmentMemo`.

### 3. The Graph (`graph/workflow.py`)
- Initialize the `StateGraph`.
- Add nodes (`planner`, `researcher`, `writer`).
- Define Edges:
    - `planner` -> `researcher` (if information is missing).
    - `planner` -> `writer` (if sufficient info exists).
    - `researcher` -> `planner` (loop back to reassess).
    - `writer` -> `END` (or `reviewer` in future).
- Compile the graph into a runnable application.

## Acceptance Criteria
- [ ] `FounderState` is strictly typed.
- [ ] The Graph compiles without errors.
- [ ] Integration Test:
    - Input: "Research Airbnb's business model."
    - Flow: Planner -> Researcher (calls tool) -> Planner -> Writer -> Output.
    - Output: A populated `InvestmentMemo` object.
