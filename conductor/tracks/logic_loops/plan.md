# Plan: The Logic Loops (LangGraph)

## Phase 1: State & Skeleton [checkpoint: 0c85105]
- [x] Task: Define Agent State dad361c
    - Update `src/foundermode/domain/state.py` with the full `FounderState` definition including `ResearchFact` lists and `InvestmentMemo`.
- [x] Task: Create Graph Skeleton 98009f4
    - Update `src/foundermode/graph/workflow.py` to initialize a `StateGraph`.
    - Create placeholder nodes (pass-throughs) to verify graph compilation.

## Phase 2: The Nodes
- [x] Task: Implement Planner Node e131218
    - Create `src/foundermode/graph/nodes/planner.py`.
    - Use LLM to analyze state and output a `ResearchPlan` or signal to write.
- [x] Task: Implement Researcher Node c7fe94d
    - Create `src/foundermode/graph/nodes/researcher.py`.
    - Integrate `TavilySearch` and `ChromaManager`.
    - Logic: Search -> Extract Facts -> Save to Memory -> Update State.
- [x] Task: Implement Writer Node 40f89cb
    - Create `src/foundermode/graph/nodes/writer.py`.
    - Logic: Query `ChromaManager` for all facts -> Generate Memo Sections -> Update `memo_draft`.

## Phase 3: Wiring & Integration [checkpoint: 50b1779]
- [x] Task: Wire the Graph 9c0b4b6
- [x] Task: Final Verification 50b1779
