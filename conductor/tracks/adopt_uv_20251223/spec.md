# Specification: Developer Experience: Adopt uv

## Context
The project currently uses standard `pip` for dependency management and manual virtual environment creation. To improve developer experience and provide an "npm-like" auto-venv experience, we will adopt `uv`.

## Requirements

### 1. Tooling Integration
- Use `uv` as the primary package manager and task runner.
- Maintain `hatchling` as the build backend in `pyproject.toml`.

### 2. Dependency Management
- Generate a `uv.lock` file to ensure reproducible environments.
- Support "auto-venv" behavior using `uv run`.

### 3. CI/CD Update
- Update GitHub Actions to use `astral-sh/setup-uv` for faster setup and execution.
- Replace `pip install` commands with `uv pip install` or `uv sync`.

### 4. Developer Workflow
- Update `README.md` or internal docs to reflect the new `uv`-based workflow.
- Ensure `pre-commit` continues to work (it can use its own isolated venvs or be run via `uv run pre-commit`).

## Acceptance Criteria
- [ ] `uv.lock` file is generated.
- [ ] `uv run pytest` executes tests successfully without manual venv activation.
- [ ] CI pipeline passes using `uv`.
- [ ] Documentation updated with `uv` commands.
