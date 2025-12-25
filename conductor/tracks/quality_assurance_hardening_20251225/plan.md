# Implementation Plan: quality_assurance_hardening_20251225

## Phase 1: Benchmark Hardening
- [ ] Task: Update `scripts/create_benchmark.py` to include 20 diverse test cases.
    - Categories: Easy (Consumer), Hard (Niche B2B), Trap (Physics), Adversarial (Fluff).
- [ ] Task: Execute the current `scripts/run_evals.py` to establish a performance baseline.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Benchmark Hardening' (Protocol in workflow.md)

## Phase 2: Journey & Quality Evaluators
- [ ] Task: Implement `PlannerEvaluator` using LangSmith Custom Evaluator + LLM-as-a-Judge.
- [ ] Task: Implement `ResearcherEvaluator` to measure Signal-to-Noise ratio.
- [ ] Task: Implement `RevisionDeltaEvaluator` to quantify the impact of the Critic node.
- [ ] Task: Implement `HallucinationEvaluator` to cross-reference claims against vector memory.
- [ ] Task: Update `foundermode/evaluation/evaluators.py` to support these new metrics.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Journey & Quality Evaluators' (Protocol in workflow.md)

## Phase 3: The "Gold Standard" Run & Analysis
- [ ] Task: Update `scripts/run_evals.py` to integrate the new LangSmith evaluators and automated tagging.
- [ ] Task: Execute the full benchmark suite and verify logging to LangSmith.
- [ ] Task: Perform a "Gold Standard" trace analysis to identify failures (Scraper, Stagnation, Inconsistency).
- [ ] Task: Conductor - User Manual Verification 'Phase 3: The Gold Standard Run & Analysis' (Protocol in workflow.md)

## Phase 4: System Optimization (The Tuning)
- [ ] Task: Address the top fail-mode identified in Phase 3 (e.g., prompt sharpening, tool adjustment).
- [ ] Task: Run a final verification pass to confirm metric improvements.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: System Optimization' (Protocol in workflow.md)
