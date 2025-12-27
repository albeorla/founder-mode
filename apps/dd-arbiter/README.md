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

## Quick Start

```bash
# From monorepo root
cd apps/dd-arbiter

# Install dependencies
uv sync

# Run the demo (once built)
uv run ddarbiter analyze path/to/cim.pdf
```

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
