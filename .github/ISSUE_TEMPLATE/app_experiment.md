---
name: App Experiment
about: Track a new app experiment in the venture studio
title: '[APP] '
labels: ['app-experiment', 'exploration']
assignees: ''
---

## App Name

Proposed name for the new app (e.g., `deal-screener`, `vendor-validator`)

## Problem / Opportunity

What problem does this app solve? What market opportunity does it address?

## Target Users

Who will use this app? Be specific about personas and use cases.

## Core Hypothesis

What assumption are we testing with this 1-2 week experiment?

**Success Metrics:**
- [ ] Metric 1 (e.g., "Can analyze a 50-page document in <5 minutes")
- [ ] Metric 2 (e.g., "Produces actionable insights validated by 3 users")
- [ ] Metric 3 (e.g., "Users willing to pay $X for this capability")

## Technical Approach

### Architecture

- **Workflow Type:** (e.g., Linear pipeline, Adversarial loop, Human-in-the-loop)
- **Key Components:** (e.g., Agents, Tools, Data sources)
- **Shared Libraries:** What will we reuse from `agentkit`?

### Estimated Scope

- **LOC:** ~200-300 lines of domain logic
- **Timeline:** 1-2 weeks
- **Dependencies:** List any new dependencies needed

## Deliverables

- [ ] App scaffolding (`apps/{app-name}/`)
- [ ] Core workflow implementation
- [ ] Basic tests (>70% coverage)
- [ ] README with setup instructions
- [ ] Demo/example usage

## Go/No-Go Criteria

How will we decide if this app is worth scaling vs. archiving?

**Go (Continue investing):**
- Criterion 1
- Criterion 2

**No-Go (Archive and move on):**
- Criterion 1
- Criterion 2

## Resources

- Related research: (links to docs, papers, etc.)
- Competitive analysis: (similar products/approaches)
- User feedback: (conversations, surveys, etc.)

## Timeline

- **Week 1:** Core implementation
- **Week 2:** Testing and user validation
- **Decision Point:** End of Week 2

## Notes

Additional context, constraints, or considerations.
