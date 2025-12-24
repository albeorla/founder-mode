# Specification: Project Configuration & CI Setup

## Context
We are initializing the `foundermode` project. This track focuses on establishing the project's build configuration, dependency management, code quality standards, and Continuous Integration (CI) pipeline using GitHub Actions.

## Requirements

### 1. Build Configuration (`pyproject.toml`)
- **Build Backend:** Hatchling.
- **Python Version:** >= 3.12.
- **Dependencies:**
    - Core: `langgraph`, `langchain`, `chromadb`, `fastapi`, `uvicorn`, `typer`, `pydantic`.
    - Tools: `beautifulsoup4`.
    - Dev: `pytest`, `ruff`, `mypy`, `pre-commit`.
- **Tool Config:**
    - Ruff for linting and formatting.
    - Pytest for testing with coverage.
    - Mypy for static type checking (strict mode).

### 2. Pre-commit Hooks (`.pre-commit-config.yaml`)
- Standard hooks: `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-toml`.
- Ruff: Linting and formatting.
- Mypy: Type checking.

### 3. CI Pipeline (`.github/workflows/ci.yml`)
- Trigger: Push and Pull Request to `main`.
- **Job 1: Quality**
    - Install dependencies.
    - Run Ruff (Lint).
    - Run Ruff (Format Check).
    - Run Mypy (Type Check).
- **Job 2: Test**
    - Depends on Quality job.
    - Run Pytest with coverage.

### 4. Project Structure
- Source code: `src/foundermode/`
- Tests: `tests/`

## Acceptance Criteria
- [ ] `pyproject.toml` exists and allows installing the project in editable mode (`pip install -e .`).
- [ ] Pre-commit hooks are configured.
- [ ] GitHub Actions workflow is defined and syntactically correct.
- [ ] `src/` and `tests/` directories exist with `__init__.py` files.
