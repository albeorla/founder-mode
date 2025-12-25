# Implementation Plan: red_team_loop_20251225

## Phase 1: Domain & Logic Preparation
- [x] Task: Update `foundermode/domain/state.py` to include `critique_history: list[str]` and `revision_count: int`.
- [x] Task: Define `CriticVerdict` schema in `foundermode/domain/schema.py` for structured LLM output.
- [x] Task: Add unit tests in `tests/test_domain_state.py` to verify state initialization and reduction logic.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Domain & Logic Preparation' (Protocol in workflow.md)

## Phase 2: The Critic Node Implementation
- [ ] Task: Create `foundermode/graph/nodes/critic.py` with the "Skeptical Partner" persona and analysis logic.
- [ ] Task: Implement `get_critic_chain()` with structured output using `gpt-4o`.
- [ ] Task: Write unit tests in `tests/test_node_critic.py` with adversarial test cases (verifying rejection of "fluffy" memos).
- [ ] Task: Conductor - User Manual Verification 'Phase 2: The Critic Node Implementation' (Protocol in workflow.md)

## Phase 3: Planner & Workflow Integration
- [ ] Task: Update `foundermode/graph/nodes/planner.py` prompt to consume and prioritize `critique_history`.
- [ ] Task: Modify `foundermode/graph/workflow.py` to include the `critic` node and the adversarial loop edge.
- [ ] Task: Implement `should_revise` conditional logic in `workflow.py` to enforce the 3-revision limit.
- [ ] Task: Write integration tests in `tests/test_red_team_integration.py` to verify the full cycle and loop termination.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Planner & Workflow Integration' (Protocol in workflow.md)

## Phase 4: Validation & Hardening
- [ ] Task: Create an adversarial benchmarking script to automate "Red Team" testing against known weak inputs.
- [ ] Task: Run full evaluation suite and verify `revision_count` and `critique_history` persistence.
- [ ] Task: Verify all changes against `mypy` and `ruff`.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Validation & Hardening' (Protocol in workflow.md)
