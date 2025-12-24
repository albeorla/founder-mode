# Plan: Developer Experience: Adopt uv

## Phase 1: uv Initialization
- [x] Task: Initialize uv lockfile c681a01
    - Run `uv lock` to generate `uv.lock` from `pyproject.toml`.
- [x] Task: Verify Auto-Venv Execution 8cdd5dd
    - Run `uv run pytest` to ensure tests pass in a managed environment.

## Phase 2: Infrastructure Update
- [ ] Task: Update CI Workflow
    - Modify `.github/workflows/ci.yml` to use `astral-sh/setup-uv`.
    - Update jobs to use `uv run` or `uv sync`.
- [ ] Task: Update Pre-commit (Optional)
    - Ensure pre-commit hooks are optimized for a `uv`-centric environment.

## Phase 3: Documentation & Verification
- [ ] Task: Update Workflow Documentation
    - Update `conductor/workflow.md` and `tech-stack.md` (if needed) to recommend `uv`.
- [ ] Task: Final Verification
    - Protocol execution from `workflow.md`.
