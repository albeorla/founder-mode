# FounderMode Documentation

**Autonomous Due Diligence Agent**

FounderMode is an AI-powered market research system that validates business ideas with "Senior Analyst" level reasoning. Unlike simple AI wrappers, it employs a multi-agent architecture that simulates a human investment analyst workflow—reading data, forming hypotheses, and actively verifying facts via web search.

## What is FounderMode?

FounderMode transforms a single-sentence business idea into a comprehensive investment memo. The system acts like having a dedicated research team that:

- **Researches** your market using real-time web search
- **Analyzes** competitors, market size, and business model viability
- **Writes** structured investment-grade reports
- **Challenges** its own conclusions through adversarial review

### Example

**Input:**
```
foundermode run "A SaaS platform that helps restaurants reduce food waste using AI predictions"
```

**Output:**
A 10+ page Investment Memo covering:
- Executive Summary with market opportunity assessment
- Market Analysis with TAM/SAM/SOM sizing
- Competitive Landscape with specific competitor analysis

---

## Who Is This For?

| User | Use Case |
|------|----------|
| **Founders** | Validate pre-deck ideas before pitching |
| **VC Associates** | Screen inbound startups efficiently |
| **Corporate Strategy** | Rapid market sizing for new initiatives |
| **Product Managers** | Research competitive landscape |

---

## Key Features

### Active Reasoning
Unlike simple summarizers, FounderMode validates claims by actively searching the web. If it claims a competitor raised $50M, it verified that fact.

### Deep Reports
Generates strategic investment memos (10+ pages) from a single prompt. Reports include citations to sources.

### Agentic Architecture
Uses cyclic workflows with self-correction. If the system can't find pricing data, it autonomously searches again with refined queries.

### Vector Memory
Semantic deduplication prevents redundant searches and enables intelligent context retrieval across research sessions.

### Red Team Review
A built-in "Critic" agent acts as a skeptical Managing Partner, rejecting weak analysis until it meets institutional standards.

### Human-in-the-Loop
Pauses before executing research to get your approval, giving you control over the investigation process.

---

## Documentation Index

| Document | Description |
|----------|-------------|
| [Getting Started](./getting-started.md) | Installation, configuration, and first run |
| [User Guide](./user-guide.md) | Detailed usage instructions and options |
| [Architecture](./architecture.md) | Technical deep-dive into system design |
| [Diagrams](./diagrams/) | PlantUML visualizations of the system |

---

## Quick Start

```bash
# Install
pip install foundermode

# Configure API keys
export OPENAI_API_KEY="your-key"
export TAVILY_API_KEY="your-key"

# Run analysis
foundermode run "Your business idea here"
```

See [Getting Started](./getting-started.md) for detailed setup instructions.

---

## How It Works (Overview)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Planner   │───▶│  Researcher │───▶│   Writer    │───▶│   Critic    │
│             │    │             │    │             │    │             │
│ Decides what│    │ Gathers data│    │ Synthesizes │    │ Reviews and │
│ to research │    │ from web    │    │ into memo   │    │ challenges  │
└─────────────┘    └─────────────┘    └─────────────┘    └──────┬──────┘
       ▲                                                        │
       │                    Feedback Loop                       │
       └────────────────────────────────────────────────────────┘
                        (if rejected, refine)
```

The system iterates until the Critic approves the analysis or maximum iterations are reached.

See [Architecture](./architecture.md) for the complete technical explanation.

---

## Output Example

FounderMode produces professional HTML reports suitable for:
- Board presentations
- Investment committee memos
- Strategic planning documents

Each section includes:
- **Citations** linking claims to sources
- **Quantitative metrics** (TAM, CAC, LTV where available)
- **Risk assessment** with specific concerns identified

---

## License

See the project root for license information.
