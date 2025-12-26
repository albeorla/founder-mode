# GRAND PLAN: From Monolith to Venture Studio

A one-person AI venture studio built on a foundation of reusable infrastructure.

---

## Vision

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           FOUNDER-MODE MONOREPO                                  │
│                    "A One-Person AI Venture Studio"                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                         APPS LAYER                                       │    │
│  │   Each app = 1-2 week experiment, ~200 lines of domain code             │    │
│  │                                                                          │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐    │    │
│  │  │ founder-mode │ │   vendor-    │ │    deal-     │ │   comp-      │    │    │
│  │  │              │ │  validator   │ │  screener    │ │   intel      │    │    │
│  │  │ Investment   │ │ Supply chain │ │ PE/VC deal   │ │ Competitor   │    │    │
│  │  │ memos for    │ │ risk assess- │ │  screening   │ │ monitoring   │    │    │
│  │  │ founders     │ │    ment      │ │              │ │              │    │    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘    │    │
│  │         │                │                │                │             │    │
│  │         └────────────────┴────────────────┴────────────────┘             │    │
│  │                                   │                                      │    │
│  └───────────────────────────────────┼──────────────────────────────────────┘    │
│                                      │                                           │
│  ┌───────────────────────────────────┼──────────────────────────────────────┐    │
│  │                         LIBS LAYER│                                       │    │
│  │                                   ▼                                       │    │
│  │  ┌─────────────────────────────────────────────────────────────────┐     │    │
│  │  │                        agentkit                                  │     │    │
│  │  │                                                                  │     │    │
│  │  │  infra/          services/        testing/        patterns/     │     │    │
│  │  │  ├─ config       ├─ llm           ├─ fixtures     ├─ WORKFLOWS  │     │    │
│  │  │  ├─ logging      ├─ search        └─ conftest     └─ council    │     │    │
│  │  │  └─ decorators   ├─ extraction                                  │     │    │
│  │  │                  └─ vector_store                                │     │    │
│  │  └─────────────────────────────────────────────────────────────────┘     │    │
│  │                                                                           │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  (future libs as needed)       │    │
│  │  │   eval-kit      │  │   deploy-kit    │                                │    │
│  │  │ LLM-as-Judge    │  │ Docker/Fly.io   │                                │    │
│  │  │ A/B testing     │  │ templates       │                                │    │
│  │  └─────────────────┘  └─────────────────┘                                │    │
│  └───────────────────────────────────────────────────────────────────────────┘    │
│                                                                                   │
│  ┌───────────────────────────────────────────────────────────────────────────┐   │
│  │                         INFRA LAYER                                        │   │
│  │                                                                            │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │   │
│  │  │   docker/   │ │    .github/ │ │   scripts/  │ │   docs/     │          │   │
│  │  │ Dockerfile  │ │  workflows/ │ │  dev setup  │ │  ADRs       │          │   │
│  │  │ compose.yml │ │  CI/CD      │ │  release    │ │  runbooks   │          │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘          │   │
│  └───────────────────────────────────────────────────────────────────────────┘   │
│                                                                                   │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## Directory Structure (Target State)

```
founder-mode/                      # Monorepo root
├── README.md                      # "What is this repo"
├── GRAND_PLAN.md                  # This document
├── pyproject.toml                 # uv workspace config (eventually)
│
├── libs/                          # Shared libraries
│   ├── agentkit/                  # Core toolkit
│   │   ├── infra/
│   │   │   ├── config.py          # Settings + test overrides
│   │   │   ├── logging.py         # Structured logging
│   │   │   └── decorators.py      # @logged, @with_fallback, etc.
│   │   ├── services/
│   │   │   ├── llm.py             # create_llm() factory
│   │   │   ├── search.py          # Tavily wrapper
│   │   │   ├── extraction.py      # Cascading scraper
│   │   │   └── vector_store.py    # ChromaDB + InMemory
│   │   ├── testing/
│   │   │   └── fixtures.py        # Pytest fixtures
│   │   ├── patterns/
│   │   │   └── WORKFLOWS.md       # Copy-paste LangGraph patterns
│   │   └── pyproject.toml
│   │
│   ├── eval-kit/                  # Future: evaluation framework
│   │   ├── judges/                # LLM-as-Judge implementations
│   │   ├── datasets/              # Test datasets
│   │   └── runners/               # Eval orchestration
│   │
│   └── deploy-kit/                # Future: deployment templates
│       ├── docker/
│       ├── fly/
│       └── modal/
│
├── apps/                          # Applications (experiments)
│   ├── founder-mode/              # Original app, refactored
│   │   ├── nodes/                 # LangGraph nodes (plain functions)
│   │   ├── prompts/               # Domain prompts
│   │   ├── schemas/               # Pydantic models
│   │   ├── workflow.py            # Graph definition
│   │   ├── cli.py                 # Entry point
│   │   └── pyproject.toml
│   │
│   ├── vendor-validator/          # Experiment #2
│   ├── deal-screener/             # Experiment #3
│   │
│   └── _template/                 # Cookiecutter for new apps
│
├── infra/                         # Shared infrastructure
│   ├── docker/
│   │   ├── Dockerfile.base        # Base image with deps
│   │   └── docker-compose.yml     # Local dev stack
│   └── scripts/
│       ├── setup-dev.sh           # Onboarding script
│       ├── new-app.sh             # Scaffold new app
│       └── release.sh             # Release automation
│
├── .github/
│   └── workflows/
│       ├── ci.yml                 # Lint, test, type-check
│       ├── release.yml            # Tag-based releases
│       └── deploy.yml             # Per-app deployment
│
└── docs/
    ├── ADR/                       # Architecture Decision Records
    │   ├── 001-toolkit-not-framework.md
    │   ├── 002-monorepo-structure.md
    │   └── ...
    └── runbooks/                  # Operational docs
```

---

## Phased Roadmap

### Phase 0: Foundation (Current Sprint)
**Goal:** Build agentkit, prove the toolkit approach works

| Task | Status |
|------|--------|
| Define toolkit philosophy (decorators > inheritance) | ✅ Done |
| Implement agentkit infra (config, logging, decorators) | 🔄 In Progress |
| Implement agentkit services (llm, search, extraction, vector_store) | 🔄 In Progress |
| Implement testing fixtures | 🔄 In Progress |
| Document workflow patterns | 🔄 In Progress |

**Exit Criteria:** Can build a new agent app in <1 day using agentkit

---

### Phase 1: First App Migration
**Goal:** Migrate founder-mode to use agentkit, validate the approach

| Task | Est |
|------|-----|
| Create `apps/founder-mode/` structure | 2h |
| Extract nodes as plain functions + decorators | 4h |
| Extract prompts to separate files | 2h |
| Wire LangGraph workflow directly (no abstractions) | 2h |
| Update CLI to use new structure | 2h |
| Verify feature parity with old version | 4h |

**Exit Criteria:** founder-mode works identically, but uses agentkit

---

### Phase 2: Second App
**Goal:** Prove rapid iteration by building vendor-validator in <1 week

| Task | Est |
|------|-----|
| Define domain schemas (VendorRisk, Assessment) | 2h |
| Write domain prompts | 4h |
| Implement nodes (reuse patterns from WORKFLOWS.md) | 4h |
| Wire workflow | 2h |
| Basic CLI | 2h |
| Test with real vendors | 4h |

**Exit Criteria:** Working vendor validator, built in <5 days

---

### Phase 3: Evaluation Framework
**Goal:** Build eval-kit to measure app quality systematically

| Task | Est |
|------|-----|
| Port LLM-as-Judge from founder-mode | 4h |
| Create evaluation datasets per app | 4h |
| Build eval runner (batch + CI integration) | 4h |
| Integrate with LangSmith for observability | 2h |
| Add eval gate to CI pipeline | 2h |

**Exit Criteria:** Every PR runs quality evals, dashboard shows trends

---

### Phase 4: Deployment Standardization
**Goal:** One-command deployment for any app

| Task | Est |
|------|-----|
| Create base Docker image with common deps | 2h |
| Fly.io deployment template | 4h |
| Modal.com deployment template (for GPU workloads) | 4h |
| Per-app config system (env + secrets) | 2h |
| `scripts/deploy.sh <app>` script | 2h |

**Exit Criteria:** `./scripts/deploy.sh vendor-validator production` works

---

### Phase 5: Customer Discovery
**Goal:** Find product-market fit for one app

| App | Target | Action |
|-----|--------|--------|
| founder-mode | Pre-seed founders | Cold outreach, offer free reports |
| vendor-validator | Procurement teams | Cold outreach, 48-hour pilot |
| deal-screener | PE associates | Warm intros, free trial |

**Process per app:**
1. Identify 20 potential customers
2. Reach out to 10
3. Deliver 3 free pilots
4. Ask for payment on 4th

**Exit Criteria:** One app has 3+ paying customers OR clear signal to kill

---

### Phase 6: Double Down or Pivot
Based on Phase 5 results:

**If winner found:**
- Extract winning app to standalone repo (if needed)
- Build proper landing page
- Implement billing (Stripe)
- Scale customer acquisition
- Consider: keep as service or build SaaS?

**If no winner:**
- Analyze feedback patterns across apps
- Generate 3 new app hypotheses
- Return to Phase 2 with new apps
- Keep cycle time <2 weeks per experiment

---

## Architecture Principles

### 1. Toolkit, Not Framework
```
Framework: "Here's how you must structure your code"  ← Constraining
Toolkit:   "Here are tools you can use as needed"     ← Enabling
```

- Use decorators instead of base classes
- Write LangGraph directly, no wrappers
- Document patterns, don't encode them

### 2. Standardize Plumbing, Keep Business Logic Raw
```
STANDARDIZE (agentkit)          RAW (apps)
─────────────────────           ─────────
Config management               Workflow structure
Logging                         Agent composition
API wrappers                    Routing logic
Test fixtures                   Domain prompts
                                Output schemas
```

### 3. Extract When Repeated 3x
- First time: Write in app
- Second time: Copy to new app
- Third time: Extract to libs/

### 4. Lazy Everything
- Lazy imports for heavy deps (Playwright, ChromaDB)
- Lazy config loading
- Lazy service initialization

---

## Business Model Options

| Model | Description | Pros | Cons |
|-------|-------------|------|------|
| **SaaS** | Monthly subscription | Recurring revenue | Requires scale |
| **Service** | Done-for-you reports | High margins, fast cash | Doesn't scale |
| **Hybrid** | Service → SaaS | Validates demand first | Complex transition |
| **Open Core** | OSS toolkit, paid apps | Community, hiring signal | Slow monetization |

**Recommended Path:**
1. Start with **Service** (validate demand with real deliverables)
2. Transition to **Hybrid** (build SaaS features customers actually request)
3. Consider **Open Core** if agentkit gets external traction

---

## Key Principles

### Speed Over Perfection
- Ship in days, not weeks
- Good enough > perfect
- Customer feedback > internal iteration
- "If you're not embarrassed by v1, you shipped too late"

### Shared Infrastructure, Unique Apps
- 80% code shared (agentkit)
- 20% code unique (domain logic)
- Every app benefits from infra improvements

### Kill Fast
- 2 weeks to validate an app idea
- No customers after outreach = kill or pivot
- Sunk cost fallacy is the enemy
- Failed experiments are data, not failures

### Compound Learning
- Every app teaches something
- Document learnings in ADRs
- Patterns that work get promoted to agentkit
- Patterns that don't get documented too (why not)

### Stay Lean
- One-person operation as long as possible
- Automate before hiring
- Revenue before fundraising
- Constraints breed creativity

---

## Success Metrics

### Library Health
| Metric | Target |
|--------|--------|
| Time to scaffold new app | <4 hours |
| Test coverage | >80% |
| Import time (no heavy deps) | <100ms |
| Breaking changes per quarter | 0 |

### App Velocity
| Metric | Target |
|--------|--------|
| New app prototype | <1 week |
| Feature iteration | <1 day |
| Bug fix to production | <1 hour |
| Apps launched per quarter | 2-3 |

### Business Traction
| Metric | Target |
|--------|--------|
| Customer conversations | 30+ in Q1 |
| Pilots delivered | 10+ in Q1 |
| Paying customers | 3+ by month 6 |
| Revenue | $1k MRR by month 6 |

---

## Timeline

```
TODAY                           3 MONTHS                        6 MONTHS
─────                           ────────                        ─────────
1 app (founder-mode)            3-4 apps tested                 1 app with traction
No customers                    20+ customer convos             5+ paying customers
Monolithic code                 Clean monorepo                  Deployment automated
"I built a thing"               "I'm testing hypotheses"        "I have a business"


6 MONTHS                        9 MONTHS                        12 MONTHS
────────                        ────────                        ─────────
1 app with traction             Growing that app                Decision point
5+ paying customers             $3-5k MRR                       $10k MRR or pivot
Deployment automated            Landing page, billing           Hire or stay solo
"I have a business"             "I'm growing a business"        "I have options"
```

---

## What This Enables

### For Building
- Test 4-5 app ideas in the time it would take to perfect one
- Every improvement to agentkit benefits all apps
- New apps start with production-grade infrastructure

### For Learning
- Rapid customer feedback loops
- A/B test different approaches across apps
- Build intuition for what works in AI products

### For Optionality
- Multiple shots on goal for product-market fit
- Portfolio approach reduces risk
- Can pivot without starting from zero
- Attractive to acquirers (proven execution)

---

## Immediate Next Actions

1. **This week:** Finish agentkit Phase 0
2. **Next week:** Migrate founder-mode (Phase 1)
3. **Week after:** Build vendor-validator (Phase 2)
4. **Parallel:** Start customer discovery conversations

---

## Open Questions (To Resolve Later)

- [ ] When to extract agentkit to separate public repo?
- [ ] Which app vertical has best risk/reward?
- [ ] Service vs SaaS pricing for first paying customers?
- [ ] Solo vs co-founder for scaling?

---

*Last updated: December 2024*
*Next review: After Phase 2 completion*
