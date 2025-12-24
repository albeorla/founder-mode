# Plan: The Logic Loops (LangGraph)

## Phase 1: State & Skeleton
- [x] Task: Define Agent State dad361c
    - Update `src/foundermode/domain/state.py` with the full `FounderState` definition including `ResearchFact` lists and `InvestmentMemo`.
- [ ] Task: Create Graph Skeleton
    - Update `src/foundermode/graph/workflow.py` to initialize a `StateGraph`.
    - Create placeholder nodes (pass-throughs) to verify graph compilation.

## Phase 2: The Nodes
- [ ] Task: Implement Planner Node
    - Create `src/foundermode/graph/nodes/planner.py`.
    - Use LLM to analyze state and output a `ResearchPlan` or signal to write.
- [ ] Task: Implement Researcher Node
    - Create `src/foundermode/graph/nodes/researcher.py`.
    - Integrate `TavilySearch` and `ChromaManager`.
    - Logic: Search -> Extract Facts -> Save to Memory -> Update State.
- [ ] Task: Implement Writer Node
    - Create `src/foundermode/graph/nodes/writer.py`.
    - Logic: Query `ChromaManager` for all facts -> Generate Memo Sections -> Update `memo_draft`.

## Phase 3: Wiring & Integration
- [ ] Task: Wire the Graph
    - Update `src/foundermode/graph/workflow.py` with real nodes and conditional edges.
    - Define the router logic (`should_continue`).
- [ ] Task: Final Verification
    - Execute the Phase Completion Verification Protocol.
