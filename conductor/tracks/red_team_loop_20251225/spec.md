# Track Spec: red_team_loop_20251225

## Overview
This track implements the "Red Team" loop for FounderMode V2. It introduces a **Critic Node** acting as a Skeptical VC Partner that reviews Investment Memos. If the memo lacks quantitative rigor or depth, the Critic rejects it, providing specific feedback that the Planner must use to re-orchestrate research.

## Functional Requirements
- **Critic Node (`critic.py`):**
    - Implementation of a new LangGraph node using a "Skeptical Partner" persona.
    - Logic to analyze the `InvestmentMemo` for quantitative metrics (CAC, LTV, Churn, TAM) and citation quality.
    - Output: A structured verdict (`approve` or `reject`) and a detailed list of `missing_data` or `improvement_areas`.
- **State Update (`state.py`):**
    - Add `critique_history: list[str]` to the `FounderState` to store historical feedback.
    - Add `revision_count: int` to prevent infinite loops (max 3 revisions).
- **Planner Integration (`planner.py`):**
    - Update the Planner prompt to consume `critique_history`.
    - Logic to prioritize "Missing Data" from the Critic when generating new research tasks while maintaining autonomous synthesis.
- **Workflow Orchestration (`workflow.py`):**
    - Insert the `critic` node after the `writer`.
    - Implement a conditional edge from `critic`:
        - If `reject` and `revision_count < 3` -> `planner`.
        - If `approve` or `revision_count >= 3` -> `END`.

## Evaluation & Success Criteria
- **Adversarial Benchmarking:** The Critic must correctly reject 100% of a test set containing deliberately "fluffy" memos.
- **Feedback Precision:** Verify via LangSmith that the Critic's "Missing Data" list accurately reflects facts not present in the vector store.
- **Loop Termination:** Unit tests must confirm that the graph terminates after exactly 3 rejections.

## Out of Scope
- Implementing the Deep Scraper (this will be a separate track).
- Changes to the UI/CLI reporting (beyond displaying the critique status).
