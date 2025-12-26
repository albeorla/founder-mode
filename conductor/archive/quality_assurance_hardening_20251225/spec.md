# Track Spec: quality_assurance_hardening_20251225

## Overview
This track transforms the FounderMode evaluation suite from a basic script into a production-grade diagnostics engine. By hardening the benchmark and implementing journey-based evaluators, we move from "Vibe Checks" to "Metric-Driven Development," ensuring the agent produces "Partner-Grade" analysis before we proceed to UI development.

## Functional Requirements
- **Benchmark Expansion:**
    - Update `scripts/create_benchmark.py` to include 20 diverse cases.
    - Ensure coverage across: Easy (Consumer), Hard (Niche B2B), Trap (Physics/Logic violations), and Adversarial (No-business-model fluff).
- **LangSmith Journey Evaluators (LLM-as-a-Judge):**
    - `PlannerEvaluator`: Analyzes search queries for "due diligence intent" (TAM, CAC, Unit Economics vs generic fluff).
    - `ResearcherEvaluator`: Measures Signal-to-Noise ratio (Valid Facts / Scraped URLs).
    - `RevisionDeltaEvaluator`: Quantifies the impact of the Critic node by measuring the increase in specific, quantitative facts between Draft V1 and Draft V2.
- **Output Quality Evaluators:**
    - `InvestorRubricEvaluator`: Standardized 5-point grading on clarity, data density, and strategic insight.
    - `HallucinationEvaluator`: Cross-references memo claims against facts stored in the vector memory.
- **Failure Mode Diagnostics:**
    - Implement automated categorization for Scraper Failures, Hallucination, Research Stagnation, and Critic Inconsistency.

## Acceptance Criteria
- `scripts/run_evals.py` executes the full 20-case benchmark without crashing.
- Results are successfully logged to LangSmith with journey metrics and failure categories.
- The system achieves a baseline score of >4.0/5.0 on the Investor Rubric and >80% pass rate on Hallucination checks.
- A "Gold Standard" trace analysis is produced, identifying the top failure mode for future optimization.

## Out of Scope
- Building the streaming web UI.
- Performance optimization for speed (focus is on quality/accuracy).
