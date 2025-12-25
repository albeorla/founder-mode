# Track Spec: quality_tuning_20251225

## Overview
This track focuses on transitioning the FounderMode agent from a functional "Walking Skeleton" to a high-quality analytical tool. The goal is to move beyond simple summarization and achieve "Senior Analyst" level reasoning, fact density, and citation accuracy through prompt engineering and formal evaluation.

## Functional Requirements
- **Planner Refinement (`planner.py`):** Update the system prompt to generate aggressive, investigative research questions targeting CAC, TAM, unit economics, and specific incumbent weaknesses.
- **Researcher Refinement (`researcher.py`):** Improve the logic for interpreting and filtering search results to ensure only high-signal data is ingested into the vector store.
- **Writer Refinement (`writer.py`):** Enforce a professional investment committee format that mandates explicit citations from retrieved vector context and prioritizes analytical depth (SWOT, moats) over generic descriptions.
- **Observability:** Ensure full integration with LangSmith for tracing reasoning loops and debugging agent transitions.

## Evaluation & Success Criteria
- **LangSmith Datasets:** Create a curated dataset of 3-5 diverse business ideas to serve as a benchmark.
- **LLM-as-a-Judge:** Implement automated evaluation in LangSmith using an "Investor Rubric" to score memos on hallucination, relevance, and analytical depth.
- **Manual Smoke Test:** Successfully execute a live run (e.g., "Uber for Dog Walking") and verify the qualitative improvements in the resulting Investment Memo.
- **Automated Structure Check:** Verify that memos consistently contain mandatory sections (Risks, Competitors, Unit Economics) and valid citations.

## Non-Functional Requirements
- **Strict Typing:** All refined prompt-handling logic must pass `mypy` and `ruff` checks.
- **Performance:** Ensure that more complex prompts do not exceed context window limits or significantly degrade latency.

## Out of Scope
- Architectural changes to the LangGraph workflow structure (focus is on prompt logic, not node connectivity).
- Introduction of new vector database providers or search tools.
