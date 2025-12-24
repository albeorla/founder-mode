# FounderMode: Roadmap Review & Strategic Planning Context

## 1. Project Context
**Product:** FounderMode
**Vision:** An autonomous market research agent that acts as a VC analyst. It actively verifies facts via web search, uses vector memory to deduplicate findings, and writes professional investment memos.
**Core Tech:** Python 3.12+, LangGraph (Orchestration), LangChain, ChromaDB (Memory), FastAPI, `uv` (Manager).

## 2. Current Draft Roadmap (from `conductor/plan.md`)
The current plan is high-level and split into three phases:

*   **Phase 1: Foundation & Memory**
    *   Initialize structure (`src/foundermode/...`).
    *   Define Domain Models (`Idea`, `MarketReport`).
    *   Implement Vector Store (`ChromaManager`).
*   **Phase 2: Research Tools**
    *   Implement Tavily Search Tool.
    *   Implement Web Scraper.
*   **Phase 3: The Agent Graph**
    *   Define Graph State.
    *   Build Analyst Node & Researcher Node.
    *   Wire LangGraph workflow.

## 3. Strategic Questions for Planning
To refine this roadmap into actionable, granular tracks, we need to answer the following:

### A. Product & Scope
1.  **The "Walking Skeleton":** What is the absolute minimum end-to-end flow we can build to prove value?
    *   *Option A:* A simple script that takes a prompt, searches Tavily, and prints a summary (No Graph, No Chroma).
    *   *Option B:* A single-node LangGraph that does the same.
    *   *Option C:* The full Analyst/Researcher loop immediately.
2.  **Report Structure:** What specific sections must the "Investment Memo" contain? (e.g., "Market Size", "Competitors", "Risks"). This defines our `MarketReport` schema.

### B. Architecture & Graph Design
3.  **Multi-Agent Hierarchy:**
    *   Should we have a "Supervisor" node that delegates to "Researcher"?
    *   Or is a simple cyclic flow (`Analyst` -> `decide_next_step` -> `Researcher` -> `Analyst`) sufficient for v1?
4.  **Memory Strategy:**
    *   How exactly does ChromaDB fit in? Is it "Long-term recall" (remembering past reports) or "Working memory" (storing facts found *during* this specific research session)?
    *   *Implication:* If it's working memory, we need a robust retrieval step before generating the report.

### C. Execution & Tracks
5.  **Track Granularity:** Is "Phase 3: The Agent Graph" too large?
    *   *Proposal:* Should we split it into "Track: Basic Single-Agent Research" vs. "Track: Multi-Agent Critique Loop"?
6.  **Observability:** We are using LangGraph. Should we integrate **LangSmith** tracing immediately in the Foundation phase to aid debugging?

## 4. Instruction for the Assistant
Based on the Context and Questions above:
1.  **Critique the Current Roadmap:** Identify risks or missing steps (e.g., where does testing happen? where is the API layer built?).
2.  **Propose a Refined Track List:** Break down the work into 4-6 specific, deliverable "Conductor Tracks" that prioritize the "Walking Skeleton" (getting to a running agent fast).
3.  **Answer the "Memory Strategy" Question:** Propose a specific pattern for how the agent interacts with ChromaDB.
