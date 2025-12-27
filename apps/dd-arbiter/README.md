# Due Diligence Arbiter

**Adversarial Multi-Model Research for Investment Thesis Stress-Testing**

[![Status](https://img.shields.io/badge/Status-Pre--MVP-yellow.svg)]()
[![Target](https://img.shields.io/badge/Target-Search%20Funds%20%7C%20PE-blue.svg)]()

---

## The Problem

AI research tools are confidently wrong. **86% of users have experienced AI hallucinations**, and the cost is staggering:

- **$67.4 billion** lost globally in 2024 due to AI hallucinations
- **712+ legal cases** with sanctions for AI-generated fake citations
- **39% of workers** spend MORE time verifying AI outputs than doing the work themselves

For investment professionals, being wrong means bad deals, lost capital, and damaged reputations.

---

## The Solution

The Due Diligence Arbiter runs **adversarial multi-model stress tests** on investment materials before you commit to full diligence.

```
Input: CIM or Management Presentation
         ↓
┌─────────────────────────────────────────┐
│  ADVERSARIAL ANALYSIS ENGINE            │
├─────────────────────────────────────────┤
│  [Bull Agent]  → Builds the growth case │
│  [Bear Agent]  → Attacks assumptions    │
│  [Arbiter]     → Synthesizes + scores   │
└─────────────────────────────────────────┘
         ↓
Output:
- Thesis Confidence Score (0-100)
- Key risks by deal-breaker potential
- Model disagreement analysis
- Suggested diligence questions
```

**You get a "Diligence Confidence Score" in 4 hours, not 4 weeks.**

---

## Target Market

### Primary: Search Funds & Independent Sponsors

| Segment | Pain | Willingness to Pay |
|---------|------|-------------------|
| **Search Fund Principals** | Review 50-100 deals to close 1. Each "real" diligence costs $20-50K. | $750-1,500/month |
| **Independent Sponsors** | Same profile, slightly larger deals. Need to move fast. | $1,000-2,000/month |
| **Family Office Investment Staff** | Small teams, direct deal flow, no time for bad deals. | $1,500-3,000/month |

### Why These Buyers?

- CIMs are **semi-public documents** (no data room access needed)
- They have **personal capital at stake**
- They **already pay** for research tools and expert networks
- Sales cycles are **1-2 months**, not 6-12 months

---

## Technical Architecture

A 5-layer adversarial research system:

| Layer | Component | Purpose |
|-------|-----------|---------|
| 1 | **Routing + Cache** | Semantic caching, complexity routing |
| 2 | **Parallel Execution** | Independent multi-model generation |
| 3 | **Uncertainty Quantification** | Semantic entropy, self-consistency |
| 4 | **Disagreement Detection** | NLI-based claim comparison |
| 5 | **Adversarial Synthesis** | Arbiter with structured output |

**Tech Stack:**
- LangGraph for orchestration
- GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro
- DeBERTa-Large-MNLI for semantic clustering
- Instructor + Pydantic for structured outputs

See [Technical Architecture](./docs/technical-architecture.md) for full details.

---

## Development Timeline

| Phase | Weeks | Deliverable |
|-------|-------|-------------|
| **POC** | 1-2 | Working demo on real CIM |
| **Discovery** | 2-3 | 2 design partners using tool |
| **Iterate** | 3-5 | Feature refinement based on feedback |
| **Revenue** | 5-8 | 3-4 paying customers ($4-5K MRR) |
| **Scale** | 8-12 | 8-12 customers ($12-18K MRR) |

**Time to ramen profitability: 6-8 weeks**

See [Development Timeline](./docs/development-timeline.md) for week-by-week breakdown.

---

## Path to Profitability

| Milestone | Revenue | Timeline |
|-----------|---------|----------|
| First paying customer | $750-1,500 | Week 5-6 |
| Ramen profitable | $4-5K MRR | Week 6-8 |
| Sustainable | $12-18K MRR | Week 8-12 |
| Fundable | $20K+ MRR | Month 4-5 |

**Costs to reach profitability: ~$600-1,000** (mostly API costs)

See [Path to Profitability](./docs/path-to-profitability.md) for detailed financial model.

---

## Documentation

| Document | Description |
|----------|-------------|
| [Market Research](./docs/market-research.md) | $67B opportunity, buyer personas, competitive landscape |
| [Technical Architecture](./docs/technical-architecture.md) | 5-layer system, code patterns, implementation guide |
| [Development Timeline](./docs/development-timeline.md) | Week-by-week execution plan |
| [Path to Profitability](./docs/path-to-profitability.md) | Financial model and customer acquisition |
| [Investment Thesis](./docs/investment-thesis.md) | Why this is fundable + pitch narrative |

---

## Development Environment Setup

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- ~5GB disk space (for ML dependencies)
- CUDA-compatible GPU (optional, for faster inference)

### Installation

#### Option 1: Docker (Recommended - No Reinstalls!)

**Best for:** Avoiding repeated dependency downloads, consistent environment

```bash
# From monorepo root
# Build once - caches all dependencies (~4GB) in Docker image
docker compose build dd-arbiter

# Run tests (uses cached dependencies)
docker compose run --rm dd-arbiter uv run pytest

# Interactive shell for development
docker compose run --rm dd-arbiter bash

# Run dd-arbiter CLI
docker compose run --rm dd-arbiter uv run ddarbiter --help
```

**Benefits:**
- ✅ Build once (15-20 min), use for weeks
- ✅ Dependencies cached in Docker image
- ✅ ML models cached in Docker volumes
- ✅ Subsequent runs: 30-60 seconds
- ✅ Consistent environment across team

**Rebuild only when dependencies change:**
```bash
docker compose build dd-arbiter --no-cache  # Force rebuild
```

#### Option 2: Local Installation (Full)

**Best for:** IDE integration, direct Python development

```bash
# From monorepo root
cd apps/dd-arbiter

# Install all dependencies including PyTorch, transformers, etc.
uv sync --all-extras --dev

# Verify installation
uv run python -c "from ddarbiter import __version__; print(f'DD-Arbiter v{__version__}')"
```

**Note:** This installs ~4GB of dependencies including:
- PyTorch (CPU or CUDA builds)
- Transformers (for DeBERTa-Large-MNLI)
- LangGraph, Instructor, Pydantic

**First install:** ~15 minutes
**Subsequent installs:** ~30 seconds (uv caches packages in `~/.cache/uv/`)

#### Option 3: CPU-Only Installation (Faster, No GPU)

```bash
# Install with CPU-only PyTorch (reduces download size)
uv sync --all-extras --dev --override torch==2.1.0+cpu

# This is sufficient for development and testing
```

#### Option 4: Minimal Installation (Testing Only)

```bash
# Install only core dependencies (excludes heavy ML models)
uv sync --dev

# Note: Some features will not work without full dependencies
```

### Configuration

Create a `.env` file in `apps/dd-arbiter/`:

```bash
# Required API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Optional Configuration
MODEL_CACHE_DIR=~/.cache/dd-arbiter  # Cache for model weights
SEMANTIC_CACHE_TTL=3600              # Cache TTL in seconds
LOG_LEVEL=INFO                        # DEBUG, INFO, WARNING, ERROR
```

### Quick Start

#### Using Docker (Recommended)

```bash
# Build the image (first time only, ~15-20 min)
docker compose build dd-arbiter

# Analyze a CIM (once POC is implemented)
docker compose run --rm dd-arbiter uv run ddarbiter analyze /workspace/path/to/cim.pdf

# Interactive mode
docker compose run --rm dd-arbiter uv run ddarbiter interactive

# Development shell
docker compose run --rm dd-arbiter bash
```

#### Using Local Installation

```bash
# Run the demo (once POC is implemented)
uv run ddarbiter analyze path/to/cim.pdf

# Run with custom models
uv run ddarbiter analyze path/to/cim.pdf --bull-model gpt-4o --bear-model claude-3-5-sonnet

# Run in interactive mode
uv run ddarbiter interactive
```

### Running Tests

#### Using Docker

```bash
# Run all tests (uses cached dependencies)
docker compose run --rm dd-arbiter uv run pytest -v

# Run with coverage
docker compose run --rm dd-arbiter uv run pytest --cov=apps/dd-arbiter --cov-report=term-missing

# Run only fast tests
docker compose run --rm dd-arbiter uv run pytest -m "not slow"

# Watch mode during development
docker compose run --rm dd-arbiter uv run pytest --testmon -f
```

#### Using Local Installation

```bash
# Run all dd-arbiter tests
uv run pytest apps/dd-arbiter/ -v

# Run with coverage
uv run pytest apps/dd-arbiter/ --cov=apps/dd-arbiter --cov-report=term-missing

# Run only fast tests (excludes model downloads)
uv run pytest apps/dd-arbiter/ -m "not slow"
```

### Development Workflow

#### Using Docker

```bash
# Start interactive development shell
docker compose run --rm dd-arbiter bash

# Inside the container, run quality checks:
uv run ruff check .
uv run ruff format .
uv run mypy .
uv run pytest -v

# Or run from host:
docker compose run --rm dd-arbiter uv run ruff check .
docker compose run --rm dd-arbiter uv run ruff format .
docker compose run --rm dd-arbiter uv run mypy .
docker compose run --rm dd-arbiter uv run pytest
```

#### Using Local Installation

```bash
# Run linting
uv run ruff check apps/dd-arbiter/

# Auto-format code
uv run ruff format apps/dd-arbiter/

# Type checking
uv run mypy apps/dd-arbiter/

# All quality checks
uv run ruff check apps/dd-arbiter/ && \
uv run ruff format apps/dd-arbiter/ && \
uv run mypy apps/dd-arbiter/ && \
uv run pytest apps/dd-arbiter/
```

### Troubleshooting

#### Import Errors

```bash
# Verify Python can find the package
uv run python -c "import sys; print(sys.path)"
uv run python -c "import ddarbiter; print(ddarbiter.__file__)"

# Reinstall if needed
uv sync --reinstall
```

#### CUDA/GPU Issues

```bash
# Check CUDA availability
uv run python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Force CPU-only mode
export CUDA_VISIBLE_DEVICES=""
```

#### Model Download Failures

```bash
# Set cache directory with more space
export HF_HOME=/path/to/large/disk/.cache/huggingface

# Download models manually
uv run python -c "from transformers import AutoModel; AutoModel.from_pretrained('microsoft/deberta-large-mnli')"
```

### CI/CD

DD-Arbiter has a **separate CI pipeline** (`.github/workflows/dd-arbiter-ci.yml`) that runs:

- **Nightly:** At 2 AM UTC
- **On changes:** To `apps/dd-arbiter/**` or `libs/agentkit/**`
- **Manual:** Via workflow_dispatch

This isolation prevents blocking the main CI pipeline with heavy dependency installation.

See [Testing Strategy](../../docs/testing-strategy.md) for details on handling heavy dependencies.

---

## Project Status

- [x] Market research validated
- [x] Technical architecture designed
- [x] Development timeline planned
- [ ] POC implementation
- [ ] Design partner acquisition
- [ ] First revenue

---

## License

[MIT](../../LICENSE)
