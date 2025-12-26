# Founder-Mode Documentation

**A One-Person AI Venture Studio**

This monorepo houses a portfolio of AI agent applications built on shared infrastructure. The goal: test multiple product hypotheses rapidly by standardizing plumbing and keeping business logic lean.

---

## What is Founder-Mode?

Founder-Mode is an **AI venture studio** approach—a monorepo containing:

1. **Apps**: Independent AI agent experiments (~200 lines of domain code each)
2. **Libs**: Shared toolkit (`agentkit`) for config, services, and testing
3. **Infra**: Common CI/CD, Docker, and deployment templates

Each app is a 1-2 week experiment targeting a specific market hypothesis. Apps share infrastructure but own their business logic.

---

## Current Apps

| App | Description | Status |
|-----|-------------|--------|
| **founder-mode** | Investment memo generator for startup ideas | Active |
| **vendor-validator** | Supply chain risk assessment | Planned |
| **deal-screener** | PE/VC deal screening | Planned |

### founder-mode (First App)

The flagship app transforms a single-sentence business idea into a comprehensive investment memo. It acts like having a dedicated research team that:

- **Researches** your market using real-time web search
- **Analyzes** competitors, market size, and business model viability
- **Writes** structured investment-grade reports
- **Challenges** its own conclusions through adversarial review

**Example:**
```bash
uv run foundermode run "A SaaS platform that helps restaurants reduce food waste"
```

**Output:** A 10+ page Investment Memo covering executive summary, market analysis, and competitive landscape.

---

## Architecture Vision

```
┌─────────────────────────────────────────────────────────────────────┐
│                       FOUNDER-MODE MONOREPO                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  APPS LAYER        Each app = 1-2 week experiment, ~200 LOC domain  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                 │
│  │ founder-mode │ │   vendor-    │ │    deal-     │  ...more        │
│  │              │ │  validator   │ │  screener    │                 │
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

## Documentation Index

| Document | Description |
|----------|-------------|
| [Monorepo Plan](./monorepo-plan.md) | Architecture vision and phased roadmap |
| [Getting Started](./getting-started.md) | Installation and first run |
| [User Guide](./user-guide.md) | Usage instructions and examples |
| [Architecture](./architecture.md) | Technical deep-dive into system design |
| [Diagrams](./diagrams/) | PlantUML visualizations |

---

## Quick Start

### Using Docker (Recommended)

```bash
git clone https://github.com/albeorla/founder-mode.git
cd founder-mode
cp .env.example .env  # Add your API keys

docker compose build
docker compose run --rm app run "Your business idea here"
```

### Using Local Installation

```bash
uv sync
uv run playwright install chromium

export OPENAI_API_KEY="your-key"
export TAVILY_API_KEY="your-key"

uv run foundermode run "Your business idea here"
```

See [Getting Started](./getting-started.md) for detailed setup instructions.

---

## Target Users

| User | Use Case |
|------|----------|
| **Founders** | Validate pre-deck ideas before pitching |
| **VC Associates** | Screen inbound startups efficiently |
| **Corporate Strategy** | Rapid market sizing for new initiatives |
| **Product Managers** | Research competitive landscape |

---

## License

See the project root for license information.
