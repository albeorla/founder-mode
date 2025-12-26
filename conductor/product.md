# Product Guide: Founder-Mode Venture Studio

## Vision

Founder-Mode is a **one-person AI venture studio**—a monorepo that houses multiple AI agent applications built on shared infrastructure. The approach enables rapid hypothesis testing: build apps in 1-2 weeks, validate with customers, double down or kill fast.

## Core Value Proposition

- **Rapid Experimentation:** Test 4-5 app ideas in the time it would take to perfect one
- **Shared Infrastructure:** 80% code shared (agentkit), 20% unique (domain logic)
- **Compound Learning:** Every app teaches something; patterns that work get promoted to agentkit

## Architecture Layers

### Apps Layer
Independent experiments, each targeting a specific market:

| App | Target Market | Value Prop |
|-----|---------------|------------|
| **founder-mode** | Pre-seed founders | Investment memo generation |
| **vendor-validator** | Procurement teams | Supply chain risk assessment |
| **deal-screener** | PE/VC associates | Deal screening automation |
| **comp-intel** | Product managers | Competitor monitoring |

### Libs Layer (agentkit)
Shared toolkit providing:
- **infra/**: Config management, logging, decorators
- **services/**: LLM, search, extraction, vector store wrappers
- **testing/**: Pytest fixtures for rapid test development
- **patterns/**: Copy-paste LangGraph workflow templates

### Infra Layer
- Docker templates for consistent environments
- CI/CD pipelines (lint, test, type-check, build)
- Deployment scripts for Fly.io/Modal

## Key Principles

### Speed Over Perfection
- Ship in days, not weeks
- Customer feedback > internal iteration
- "If you're not embarrassed by v1, you shipped too late"

### Kill Fast
- 2 weeks to validate an app idea
- No customers after outreach = kill or pivot
- Failed experiments are data, not failures

### Toolkit, Not Framework
- Decorators over base classes
- LangGraph directly, no wrappers
- Document patterns, don't encode them

## Current Focus: founder-mode App

The first app generates investment memos from business ideas. Key features:

- **Active Reasoning:** Validates claims by searching the web
- **Deep Reports:** 10+ page memos from a single prompt
- **Agentic Architecture:** Cyclic workflows with self-correction
- **Vector Memory:** Semantic deduplication via ChromaDB
- **Red Team Review:** Adversarial critic that rejects weak analysis
- **Human-in-the-Loop:** Approval gates before execution

## Success Metrics

### Library Health
| Metric | Target |
|--------|--------|
| Time to scaffold new app | <4 hours |
| Test coverage | >80% |
| Import time (no heavy deps) | <100ms |

### App Velocity
| Metric | Target |
|--------|--------|
| New app prototype | <1 week |
| Feature iteration | <1 day |
| Bug fix to production | <1 hour |

### Business Traction
| Metric | Target |
|--------|--------|
| Customer conversations | 30+ in Q1 |
| Pilots delivered | 10+ in Q1 |
| Paying customers | 3+ by month 6 |

## Reference

See [docs/monorepo-plan.md](../docs/monorepo-plan.md) for the complete roadmap and architecture details.
