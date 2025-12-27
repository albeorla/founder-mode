# Testing Strategy

## Overview

This document outlines the testing strategy for the Founder-Mode monorepo, with special attention to handling applications with heavy dependencies like ML/AI libraries.

## Test Organization

### Test Markers

All tests should be marked appropriately to enable selective execution:

```python
import pytest

@pytest.mark.unit
def test_fast_isolated_unit():
    """Fast, isolated unit tests with no external dependencies."""
    pass

@pytest.mark.integration
def test_with_mocked_services():
    """Tests with mocked external services (APIs, databases, etc.)."""
    pass

@pytest.mark.e2e
def test_full_workflow():
    """Full end-to-end workflow tests."""
    pass

@pytest.mark.slow
def test_long_running():
    """Tests that take >1 second to run."""
    pass
```

### Running Tests

#### Standard Development (Excludes Heavy Apps)

```bash
# Fast feedback loop during development
uv run pytest --testmon -n auto --ignore=apps/dd-arbiter

# Run only fast tests
uv run pytest -m "not slow" --ignore=apps/dd-arbiter

# Re-run failed tests first
uv run pytest --ff --ignore=apps/dd-arbiter
```

#### Heavy ML Apps (DD-Arbiter, etc.)

```bash
# Run dd-arbiter tests separately
uv run pytest apps/dd-arbiter/ -v

# Run with coverage
uv run pytest apps/dd-arbiter/ --cov=apps/dd-arbiter --cov-report=term-missing
```

#### Full Test Suite

```bash
# Run everything (use in CI or before major releases)
uv run pytest -n auto --cov=libs --cov=apps
```

## CI/CD Strategy

### Main CI Pipeline (`.github/workflows/ci.yml`)

**Runs on:** Every push and PR to main

**Scope:**
- `libs/agentkit/` - Shared libraries
- `apps/founder-mode/` - Lightweight applications
- Excludes: Heavy ML apps (`apps/dd-arbiter/`)

**Jobs:**
1. **Code Quality** - Linting, formatting, type checking
2. **Fast Tests** - Unit tests with `-m "not slow"`
3. **Full Tests + Coverage** - All tests with coverage reporting
4. **Docker Build** - Verify Docker image builds

### DD-Arbiter CI Pipeline (`.github/workflows/dd-arbiter-ci.yml`)

**Runs on:**
- Schedule: Nightly at 2 AM UTC
- Changes to `apps/dd-arbiter/**` or `libs/agentkit/**`
- Manual trigger (workflow_dispatch)

**Scope:**
- `apps/dd-arbiter/` only
- Includes heavy ML dependencies (~4GB PyTorch/CUDA)

**Jobs:**
1. **Test DD-Arbiter** - Full test suite with coverage
2. **Smoke Test** - Quick import checks

**Rationale:**
- Isolates expensive dependency installation (30+ min)
- Prevents blocking fast feedback on main codebase
- Still catches integration issues via scheduled runs

## Handling Heavy Dependencies

### When to Separate CI

Create a separate CI workflow when an app:
- Has >1GB of dependencies
- Takes >10 minutes to install dependencies
- Requires specialized hardware (GPU, CUDA)
- Has dependencies incompatible with other apps

### Pattern for Heavy Apps

```
apps/
├── my-heavy-app/
│   ├── README.md              # Document why it's separate
│   ├── pyproject.toml         # Isolated dependencies
│   ├── .python-version        # Pin Python version
│   └── tests/                 # Full test coverage
│       └── conftest.py        # Shared fixtures
```

**CI Configuration:**
```yaml
# .github/workflows/my-heavy-app-ci.yml
on:
  schedule:
    - cron: '0 2 * * *'  # Nightly
  push:
    paths:
      - 'apps/my-heavy-app/**'
      - 'libs/agentkit/**'
  workflow_dispatch:
```

## Test Coverage Requirements

### Minimum Coverage Targets

- **Libraries (`libs/`)**: 80% coverage
- **Applications (`apps/`)**: 70% coverage
- **Critical paths**: 90% coverage

### Coverage Reporting

```bash
# Generate HTML report for detailed review
uv run pytest --cov=libs --cov=apps --cov-report=html --ignore=apps/dd-arbiter

# View in browser
open htmlcov/index.html
```

## Best Practices

### 1. Test Isolation

- Use fixtures from `libs/agentkit/testing/`
- Mock external services (APIs, databases)
- Never rely on test execution order

### 2. Fast Feedback

- Keep unit tests under 100ms
- Mark slow tests with `@pytest.mark.slow`
- Use `pytest-testmon` for incremental testing

### 3. Parallel Execution

- Design tests to run in parallel (`-n auto`)
- Avoid shared state between tests
- Use temporary directories for file operations

### 4. Mocking

```python
from agentkit.testing import mock_llm, mock_chroma_manager

def test_with_mocks(mock_llm, mock_chroma_manager):
    """Use shared fixtures for consistent mocking."""
    mock_llm.return_value = "Mocked response"
    # Test implementation
```

### 5. Environment Variables

```python
import os
import pytest

@pytest.fixture(autouse=True)
def mock_api_keys(monkeypatch):
    """Auto-mock API keys for all tests."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
```

## Troubleshooting

### Tests Failing in CI but Passing Locally

1. Check for missing environment variables
2. Verify dependency versions match (`uv lock --check`)
3. Run with same Python version as CI (3.12)
4. Use `--ignore-glob="**/__pycache__/**"` to exclude cache

### Slow Test Suite

1. Identify slow tests: `pytest --durations=10`
2. Mark them: `@pytest.mark.slow`
3. Run fast tests first: `pytest -m "not slow"`
4. Optimize or parallelize slow tests

### Import Errors in Heavy Apps

1. Ensure dependencies installed: `uv sync --all-extras`
2. Check Python path: `uv run python -c "import sys; print(sys.path)"`
3. Verify package structure: `uv run python -c "import ddarbiter; print(ddarbiter.__file__)"`

## Future Improvements

- [ ] Set up GPU runners for ML-heavy tests
- [ ] Implement contract testing between apps and libs
- [ ] Add mutation testing for critical paths
- [ ] Create performance benchmarking suite
- [ ] Set up visual regression testing for UI components

## References

- [pytest documentation](https://docs.pytest.org/)
- [pytest-xdist (parallel execution)](https://pytest-xdist.readthedocs.io/)
- [pytest-testmon (incremental testing)](https://testmon.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
