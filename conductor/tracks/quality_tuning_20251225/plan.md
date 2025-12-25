# Implementation Plan: quality_tuning_20251225

## Phase 1: Evaluation Infrastructure & Benchmarking
- [x] Task: Create LangSmith benchmark dataset with 3-5 diverse business ideas.
- [x] Task: Implement "Investor Rubric" evaluator (LLM-as-a-Judge) in LangSmith.
- [x] Task: Develop automated structure tests (e.g., checking for required sections and citation formats).
- [x] Task: Conductor - User Manual Verification 'Phase 1: Evaluation Infrastructure' (Protocol in workflow.md)

## Phase 2: Core Agent Logic Refinement
- [x] Task: Refine `planner.py` system prompt to prioritize unit economics, CAC, and incumbent analysis.
- [x] Task: Refine `researcher.py` interpretation logic to filter for high-signal data before vector ingestion.
- [x] Task: Refine `writer.py` template to enforce professional committee formatting and mandatory citations.
- [x] Task: Verify refinements against `mypy` and `ruff`.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Core Agent Logic Refinement' (Protocol in workflow.md)

## Phase 3: Quality Validation & Tuning
- [ ] Task: Run full evaluation suite against the LangSmith benchmark dataset.
- [ ] Task: Execute manual smoke test ("Uber for Dog Walking") and archive the result.
- [ ] Task: Analyze evaluation failures and perform final prompt tuning.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Quality Validation & Tuning' (Protocol in workflow.md)
