# Founder-Mode

**A One-Person AI Venture Studio**

[![CI](https://github.com/albeorla/founder-mode/actions/workflows/ci.yml/badge.svg)](https://github.com/albeorla/founder-mode/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

This monorepo houses a **portfolio of AI agent applications** built on shared infrastructure. The goal: test multiple product hypotheses rapidly by standardizing plumbing and keeping business logic lean.

---

## Vision

```
┌─────────────────────────────────────────────────────────────────────┐
│                       FOUNDER-MODE MONOREPO                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  APPS LAYER        Each app = 1-2 week experiment, ~200 LOC domain  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                 │
│  │ founder-mode │ │   vendor-    │ │    deal-     │  ...more        │
│  │              │ │  validator   │ │  screener    │                 │
│  │ Investment   │ │ Supply chain │ │ PE/VC deal   │                 │
│  │ memos        │ │ risk assess  │ │  screening   │                 │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘                 │
│         └────────────────┼────────────────┘                         │
│                          ▼                                          │
│  LIBS LAYER       ┌─────────────────────────────────────────┐       │
│                   │              agentkit                    │       │
│                   │  infra/ │ services/ │ testing/ │ patterns│       │
│                   └─────────────────────────────────────────┘       │
│                                                                     │
│  INFRA LAYER      docker/ │ .github/ │ scripts/ │ docs/             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Core Philosophy

**Toolkit, Not Framework**
- Use decorators instead of base classes
- Write LangGraph directly, no wrappers
- Document patterns, don't encode them

**Standardize Plumbing, Keep Business Logic Raw**
- `agentkit`: Config, logging, API wrappers, test fixtures
- `apps/`: Workflow structure, prompts, domain schemas

**Extract When Repeated 3x**
- First time: write in app
- Second time: copy to new app
- Third time: extract to libs/

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Runtime** | Python 3.12+ |
| **Orchestration** | [LangGraph](https://langchain-ai.github.io/langgraph/) — stateful, cyclic workflows |
| **Validation** | [Pydantic](https://docs.pydantic.dev/) — strict schemas |
| **Memory** | [ChromaDB](https://www.trychroma.com/) — vector storage |
| **Search** | [Tavily API](https://tavily.com/) — AI-optimized search |
| **Scraping** | [Playwright](https://playwright.dev/) — JS-heavy site fallback |
| **Observability** | [LangSmith](https://smith.langchain.com/) — tracing & evals |

---

## Current Apps

| App | Description | Status |
|-----|-------------|--------|
| **founder-mode** | Investment memo generator for startup ideas | Active |

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) (Recommended)
- Python 3.12+ & [uv](https://github.com/astral-sh/uv) (For local development)

### Quick Start (Docker)

This is the "Happy Path" that ensures all dependencies (browsers, OS libraries) are correctly configured.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/albeorla/founder-mode.git
    cd founder-mode
    ```

2.  **Configure Environment:**
    Copy the example environment file and add your API keys.
    ```bash
    cp .env.example .env
    ```
    *   `OPENAI_API_KEY`: Required for LLM.
    *   `TAVILY_API_KEY`: Required for web search.
    *   `MODEL_NAME`: Optional. Defaults to `gpt-4o`. Can use any OpenAI-compatible model.

3.  **Run the Agent:**
    ```bash
    docker compose build
    docker compose run --rm app run "Uber for Dog Walking"
    ```

### Local Development

1.  **Install dependencies:**
    ```bash
    uv sync
    ```

2.  **Install Playwright Browsers:**
    ```bash
    uv run playwright install chromium
    ```

3.  **Run the Agent:**
    ```bash
    uv run foundermode run "Uber for Dog Walking"
    ```

4.  **Start the API Server:**
    ```bash
    uv run uvicorn foundermode.api.server:app --reload
    ```
    API docs available at: `http://localhost:8000/docs`

## Project Structure

```
founder-mode/                      # Monorepo root
├── src/foundermode/               # Main application
│   ├── api/                       # CLI (Typer) and REST API (FastAPI)
│   ├── domain/                    # State and schema definitions
│   ├── graph/                     # LangGraph workflow
│   │   └── nodes/                 # Agent nodes (planner, researcher, writer, critic)
│   ├── tools/                     # Search, scraping, reporting
│   ├── memory/                    # ChromaDB vector storage
│   └── evaluation/                # LLM-as-Judge evaluators
│
├── libs/agentkit/                 # Shared toolkit library
│   ├── infra/                     # config, logging, decorators
│   ├── services/                  # llm, search, extraction, vector_store
│   ├── testing/                   # pytest fixtures
│   └── patterns/                  # WORKFLOWS.md — copy-paste LangGraph patterns
│
├── tests/                         # Test suite
├── docs/                          # Documentation
├── .github/workflows/             # CI/CD pipelines
└── conductor/                     # Project management
```

---

## Development & Testing

Test-driven development with optimized execution.

### Running Tests

```bash
# Standard test run
uv run pytest

# Fast development loop - only run tests affected by your changes
uv run pytest --testmon

# Parallel execution (uses all CPU cores)
uv run pytest -n auto

# Combine both for maximum speed
uv run pytest --testmon -n auto

# Skip slow tests during rapid iteration
uv run pytest -m "not slow"

# Re-run failed tests first
uv run pytest --ff
```

### Test Markers

Tests are organized with markers for selective execution:

| Marker | Description | Example |
|--------|-------------|---------|
| `@pytest.mark.unit` | Fast isolated unit tests | `pytest -m "unit"` |
| `@pytest.mark.integration` | Tests with mocked external services | `pytest -m "integration"` |
| `@pytest.mark.e2e` | Full end-to-end workflow tests | `pytest -m "e2e"` |
| `@pytest.mark.slow` | Long-running tests | `pytest -m "not slow"` |

### Coverage & Quality

```bash
# Run with coverage report
uv run pytest --cov=foundermode --cov-report=term-missing

# Generate HTML coverage report
uv run pytest --cov=foundermode --cov-report=html  # Opens htmlcov/index.html

# Full CI-style run (parallel + coverage)
uv run pytest -n auto --cov=foundermode
```

### Container & Integration Tests

```bash
# Run container integration tests
docker compose run --rm app pytest tests/container/

# Run only integration tests
uv run pytest -m "integration"
```

### Code Quality

```bash
# Linting & Formatting
uv run ruff check .
uv run ruff format .

# Type Checking
uv run mypy src/
```

### Shared Test Fixtures

The `tests/conftest.py` provides reusable fixtures to reduce boilerplate:

```python
def test_example(base_state, mock_chroma_manager):
    """Example using shared fixtures."""
    base_state["research_question"] = "My test question"
    # mock_chroma_manager is pre-configured
```

Available fixtures: `base_state`, `research_state`, `state_with_facts`, `sample_facts`, `mock_llm`, `mock_chroma_manager`, `mock_tavily_search`, `mock_deep_scrape`, `patch_chroma`, `patch_tavily`

### Evaluations (LangSmith)

Run the evaluation benchmark to measure output quality:

```bash
# Requires LANGCHAIN_API_KEY
uv run python scripts/create_benchmark.py  # Create dataset (once)
uv run python scripts/run_evals.py         # Run evaluations
uv run python scripts/adversarial_bench.py # Run adversarial testing
```

Results are tracked in LangSmith for experiment comparison. See [User Guide](./docs/user-guide.md) for details.

---

## Documentation

| Document | Description |
|----------|-------------|
| [Monorepo Plan](./docs/monorepo-plan.md) | Architecture vision and phased roadmap |
| [Getting Started](./docs/getting-started.md) | Installation and first run |
| [User Guide](./docs/user-guide.md) | Usage instructions and examples |
| [Architecture](./docs/architecture.md) | Technical deep-dive |

---

## Contributing

1. Read [docs/monorepo-plan.md](./docs/monorepo-plan.md) to understand the architecture
2. Check `conductor/` for current project management and tracks
3. Create a feature branch
4. Write tests first (TDD)
5. Submit a Pull Request

---

## License

[MIT](LICENSE)
