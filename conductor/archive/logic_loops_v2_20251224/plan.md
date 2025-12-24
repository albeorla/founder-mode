# Implementation Plan: logic_loops_v2

This plan outlines the transition to real agent logic, integrated memory, and a strict branch-based workflow.

## Phase 1: Environment Setup & Hygiene
- [x] **Task: Setup Output Management**
    - [x] Create `.out/` directory.
    - [x] Update `.gitignore` to ignore `.out/`.
    - [x] Move `test_memo.html`, `test_idea_memo.html`, and `my_idea_memo.html` to `.out/`.
- [x] **Task: Implement Configuration Management**
    - [x] Create `src/foundermode/config.py`.
    - [x] Write tests in `tests/test_config.py` for environment variable loading and validation.
    - [x] Implement `Settings` class using `pydantic-settings`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Environment Setup & Hygiene' (Protocol in workflow.md)

## Phase 2: Working Memory Integration
- [x] **Task: Enhanced Search Tool**
    - [x] Write tests in `tests/test_search_memory.py` for search-as-memory and deduplication logic.
    - [x] Update `src/foundermode/tools/search.py` to check `ChromaDB` before calling `Tavily`.
    - [x] Implement automatic upsert, metadata tagging, and similarity-based deduplication.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Working Memory Integration' (Protocol in workflow.md)

## Phase 3: Logic Loops & Dynamic Fallback
- [x] **Task: Implement Planner Node**
    - [x] Write tests for Planner logic and fallback behavior.
    - [x] Implement `Planner` logic in `src/foundermode/graph/nodes/planner.py` with dynamic fallback to mock data.
- [x] **Task: Implement Researcher Node**
    - [x] Write tests for Researcher logic and fallback behavior.
    - [x] Implement `Researcher` logic in `src/foundermode/graph/nodes/researcher.py` with dynamic fallback to mock data.
- [ ] **Task: Implement Writer Node**
    - [ ] Write tests for Writer logic (Markdown synthesis) and fallback behavior.
    - [ ] Implement `Writer` logic in `src/foundermode/graph/nodes/writer.py` with dynamic fallback to mock data.
- [x] **Task: Graph Orchestration**
    - [x] Update `src/foundermode/graph/workflow.py` to wire the real nodes into the cyclic graph.
    - [x] Verify graph topology and state transitions via integration tests.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Logic Loops & Dynamic Fallback' (Protocol in workflow.md)

## Phase 4: Final Verification
- [x] **Task: End-to-End Integration Testing**
    - [x] Run full research cycle with valid API keys and verify ChromaDB ingestion.
    - [x] Run full research cycle with missing API keys and verify graceful fallback.
- [x] Task: Conductor - User Manual Verification 'Phase 4: Final Verification' (Protocol in workflow.md)
