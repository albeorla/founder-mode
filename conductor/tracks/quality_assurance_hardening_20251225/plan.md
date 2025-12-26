# Implementation Plan: quality_assurance_hardening_20251225

## Phase 1: Benchmark Hardening
- [x] Task: Update `scripts/create_benchmark.py` to include 20 diverse test cases.
    - Categories: Easy (Consumer), Hard (Niche B2B), Trap (Physics), Adversarial (Fluff).
- [x] Task: Execute the current `scripts/run_evals.py` to establish a performance baseline.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Benchmark Hardening' (Protocol in workflow.md)

## Phase 2: Journey & Quality Evaluators
- [x] Task: Implement `PlannerEvaluator` using LangSmith Custom Evaluator + LLM-as-a-Judge.
- [x] Task: Implement `ResearcherEvaluator` to measure Signal-to-Noise ratio.
- [x] Task: Implement `RevisionDeltaEvaluator` to quantify the impact of the Critic node.
- [x] Task: Implement `HallucinationEvaluator` to cross-reference claims against vector memory.
- [x] Task: Update `foundermode/evaluation/evaluators.py` to support these new metrics.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Journey & Quality Evaluators' (Protocol in workflow.md)

## Phase 3: The "Gold Standard" Run & Analysis
- [x] Task: Update `scripts/run_evals.py` to integrate the new LangSmith evaluators and automated tagging.
- [x] Task: Execute the full benchmark suite and verify logging to LangSmith.
- [x] Task: Perform a "Gold Standard" trace analysis to identify failures (Scraper, Stagnation, Inconsistency).
- [x] Task: Conductor - User Manual Verification 'Phase 3: The Gold Standard Run & Analysis' (Protocol in workflow.md)

## Phase 4: System Optimization (The Tuning)
- [x] Task: Address the top fail-mode identified in Phase 3 (e.g., prompt sharpening, tool adjustment).
- [x] Task: Run a final verification pass to confirm metric improvements.
- [x] Task: Conductor - User Manual Verification 'Phase 4: System Optimization' (Protocol in workflow.md)
