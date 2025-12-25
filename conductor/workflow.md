# Project Workflow

## Guiding Principles

1. **The Plan is the Source of Truth:** All work must be tracked in `plan.md`.
2. **Continuous Delivery (Local):** We use short-lived feature branches and merge locally after verification. Main is always deployable.
3. **Test-Driven Development:** Write tests first. Green tests = Mergeable.
4. **Production Artifacts:** Docker is our deployment target, but `uv` is our development driver.
5. **Output Isolation:** All generated artifacts (reports, logs) must be written to `.out/` and ignored by git.

## Task Workflow

### 1. Select & Branch
- **Pick Task:** Select the next task from `plan.md`.
- **Branch:** Create a branch `task/<description>` (e.g., `task/implement-planner`).

### 2. Implementation Loop (Red-Green-Refactor)
- **Red:** Write failing tests that define the expected behavior.
- **Green:** Implement the code to pass the tests.
- **Refactor:** Clean up code and ensure linter compliance (`ruff`, `mypy`).

### 3. Verification
- **Run Tests:** `uv run pytest` (Ensure all pass).
- **Run Checks:** `pre-commit run --all-files` (Ensure style/types).
- **Check CI:** If pushed, verify pipeline health with `gh run list`.

### 4. Merge & Finalize
- **Merge:** Switch to `main` and merge the task branch (`git merge task/...`).
- **Cleanup:** Delete the task branch.
- **Record:** Update `plan.md` marking the task as `[x]`.

## Phase Completion Protocol

**Trigger:** executed when a Phase in `plan.md` is complete.

1. **Full Suite:** Run the entire test suite `CI=true uv run pytest`.
2. **Docker Check:** Build the container to ensure deployability: `docker build . -t foundermode`.
3. **Checkpoint:**
    - Create an empty commit: `git commit --allow-empty -m "conductor(checkpoint): Phase <NAME> Complete"`
    - Tag it (optional) or just note the hash in `plan.md`.

## Tooling

### Development
- **Install:** `uv sync`
- **Test:** `uv run pytest`
- **Lint/Format:** `uv run ruff check` / `uv run ruff format`
- **Type Check:** `uv run mypy src/`

### Deployment (Docker)
- **Build:** `docker build -t foundermode .`
- **Run:** `docker run --env-file .env foundermode run "Idea"`
