# Founder-Mode Documentation

**A One-Person AI Venture Studio**

Rapidly test AI agent product ideas using shared infrastructure. Currently in research phase, seeking the right opportunity for VC-scale growth.

---

## Quick Links

| I want to... | Go to |
|--------------|-------|
| Understand what this is | [Value Proposition](./value-proposition.md) |
| Set up and run | [Getting Started](./getting-started.md) |
| Learn how to use it | [User Guide](./user-guide.md) |
| Understand the architecture | [Architecture](./architecture.md) |
| See the roadmap | [Monorepo Plan](./monorepo-plan.md) |
| View diagrams | [Diagrams](./diagrams/) |

---

## What is Founder-Mode?

**The Problem**: Finding product-market fit takes too long. Most startups spend months building something nobody wants.

**The Solution**: A monorepo with shared infrastructure (agentkit) that lets us build new AI agent apps in 1-2 weeks. We test ideas rapidly until we find one worth scaling.

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│  YOUR QUESTION  →  AI Agents  →  Research + Analysis  →  OUTPUT │
│                                                                 │
│  "Key trends in energy storage?"  →  Planner → Researcher →    │
│                         Writer → Critic → Structured Analysis   │
└─────────────────────────────────────────────────────────────────┘
```

The example app (founder-mode) demonstrates multi-agent workflows:
1. **Planner** decides what to research
2. **Researcher** searches the web and extracts facts
3. **Writer** synthesizes a structured memo
4. **Critic** reviews for quality (loops back if weak)

---

## Current Phase

**Research & Exploration** — Identifying the right AI agent opportunity.

## Apps

| App | What it does | Status |
|-----|--------------|--------|
| **founder-mode** | Example: Multi-agent research with adversarial critique | Proof-of-concept |

---

## The Stack

| Component | Technology |
|-----------|------------|
| Orchestration | LangGraph (stateful, cyclic workflows) |
| LLM | OpenAI GPT-4o |
| Search | Tavily API |
| Memory | ChromaDB (vector storage) |
| API | FastAPI + Typer CLI |

---

## 5-Minute Start

```bash
# Clone
git clone https://github.com/albeorla/founder-mode.git
cd founder-mode

# Configure
cp .env.example .env  # Add your API keys

# Run
docker compose build
docker compose run --rm app run "Your business idea here"
```

See [Getting Started](./getting-started.md) for detailed instructions.

---

## Project Structure

```
founder-mode/
├── src/foundermode/    # Main application code
├── libs/agentkit/      # Shared toolkit library
├── tests/              # Test suite
├── docs/               # You are here
└── conductor/          # Project management
```

---

## Documentation Index

### For Users
- **[Getting Started](./getting-started.md)** - Install, configure, run your first analysis
- **[User Guide](./user-guide.md)** - CLI options, API usage, best practices

### For Developers
- **[Architecture](./architecture.md)** - System design, agents, memory, tools
- **[Monorepo Plan](./monorepo-plan.md)** - Vision, roadmap, architecture principles
- **[AgentKit](../libs/agentkit/README.md)** - Shared library documentation

### Visual Guides
- **[Diagrams](./diagrams/)** - PlantUML visualizations of system components

---

## Contributing

1. Read the [Architecture](./architecture.md) to understand the system
2. Check [Monorepo Plan](./monorepo-plan.md) for current priorities
3. Follow TDD - write tests first
4. Run `uv run pytest && uv run ruff check` before submitting

---

[← Back to Repository](../README.md)
