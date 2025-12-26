# FounderMode 🚀

**The Autonomous Due Diligence Agent**

[![CI](https://github.com/albeorla/founder-mode/actions/workflows/ci.yml/badge.svg)](https://github.com/albeorla/founder-mode/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**FounderMode** is an autonomous market research agent that validates business ideas end-to-end. Unlike simple wrapper tools, it employs a **multi-agent architecture** to simulate a human investment analyst: reading data, forming hypotheses, and actively verifying facts via web search.

---

## 🌟 Core Value Proposition

- **🧠 Active Reasoning:** It doesn't just summarize; it actively validates claims by searching the web.
- **📑 Deep Reports:** Generates strategic investment memos (10+ pages) from a single one-sentence prompt.
- **🔄 Agentic Architecture:** Uses cyclic graphs to self-correct (e.g., "I couldn't find pricing, I'll look again").
- **💾 Vector-Native Memory:** Uses embeddings (ChromaDB) to deduplicate and cluster semantically.
- **🔍 Research Agent:** A dedicated agent that uses tools (Tavily) to fact-check assumptions.
- **👨‍⚖️ Critic Agent:** A built-in adversarial reviewer that challenges weak analysis until it meets institutional standards.
- **🌐 Multi-Stage Scraper:** Playwright-powered fallback scraper for JavaScript-heavy sites when standard requests fail.

## 🛠 Tech Stack

Built with the **"Senior AI Engineer"** stack:

*   **Runtime:** Python 3.12+
*   **Orchestration:** [LangGraph](https://langchain-ai.github.io/langgraph/) (Stateful, cyclic multi-agent workflows)
*   **Framework:** [LangChain](https://www.langchain.com/) (Components & Interfaces)
*   **Validation:** [Pydantic](https://docs.pydantic.dev/) (Strict data & config validation)
*   **Memory:** [ChromaDB](https://www.trychroma.com/) (Local persistent vector storage)
*   **Search:** [Tavily API](https://tavily.com/) (Optimized for AI agents)
*   **Scraping:** [Playwright](https://playwright.dev/) (Browser automation for JS-heavy sites)
*   **Observability:** [LangSmith](https://smith.langchain.com/) (Tracing & Debugging)

## 🚀 Getting Started

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

## 📂 Project Structure

```
founder-mode/
├── conductor/           # Project management & specifications (Conductor framework)
├── docs/                # Comprehensive documentation
│   ├── architecture.md  # Technical deep-dive into system design
│   ├── getting-started.md
│   ├── user-guide.md
│   └── diagrams/        # PlantUML visualizations
├── scripts/             # Utility scripts
│   ├── create_benchmark.py   # Create LangSmith evaluation datasets
│   ├── run_evals.py          # Run evaluation benchmarks
│   └── adversarial_bench.py  # Adversarial testing suite
├── src/
│   └── foundermode/
│       ├── api/         # FastAPI endpoints & CLI entry points
│       ├── domain/      # Pydantic models (Schema) & State definitions
│       ├── evaluation/  # LangSmith evaluators
│       ├── graph/       # LangGraph workflow & Nodes (Planner, Researcher, Writer, Critic)
│       ├── memory/      # Vector Store (ChromaDB) integration
│       ├── tools/       # External tools (Tavily Search, Multi-stage Scraper)
│       └── utils/       # Shared utilities (logging, etc.)
├── tests/               # Pytest suite (unit, integration, container, e2e)
│   └── container/       # Docker container integration tests
├── .github/             # GitHub Actions CI workflows
└── pyproject.toml       # Project configuration & dependencies
```

## 🧪 Development & Testing

We follow a strictly **Test-Driven Development (TDD)** workflow with optimized test execution.

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

## 📖 Documentation

Comprehensive documentation is available in the `docs/` directory:

| Document | Description |
|----------|-------------|
| [Getting Started](./docs/getting-started.md) | Installation, configuration, and first run |
| [User Guide](./docs/user-guide.md) | Detailed usage instructions, options, and examples |
| [Architecture](./docs/architecture.md) | Technical deep-dive into system design |
| [Diagrams](./docs/diagrams/) | PlantUML visualizations of the workflow |

## 🤝 Contributing

1.  Read the `conductor/workflow.md` to understand our development process.
2.  Create a feature branch.
3.  Write tests first (Red).
4.  Implement the feature (Green).
5.  Refactor and ensure all checks pass.
6.  Submit a Pull Request.

## 📄 License

[MIT](LICENSE)
