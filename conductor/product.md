# Product Guide: Founder-Mode Engine

## Vision
**"AI Agents for Knowledge Work"**

Founder-Mode is an AI agent platform that generates deep, structured analysis by orchestrating multiple specialized agents. Unlike single-shot LLM wrappers, it uses a **Cyclic Multi-Agent Graph** to research, synthesize, and adversarially critique complex topics.

## Core Value Proposition

### 1. The "Cyclic Agent" Architecture
A multi-pass approach where agents build on each other's work:
- **Planner:** Breaks down complex questions into research tasks
- **Researcher:** Gathers evidence from web search and document extraction
- **Writer:** Synthesizes findings into structured output
- **Critic:** Reviews for quality and logical gaps (loops back if weak)

### 2. The "Critic" Advantage
The architecture leverages an **Adversarial Critic Node**. Quality comes from iteration.
- *Standard AI:* Single-pass response, no self-review
- *Founder-Mode:* Multi-pass with adversarial critique, catches gaps and inconsistencies

### 3. Toolkit, Not Framework
- **Decorators over inheritance:** Use `@logged`, `@with_retry`, not base classes
- **LangGraph directly:** No abstraction wrappers, full control
- **Pattern documentation:** Copy-paste workflows, not encoded constraints

## Architecture Layers

### Application Layer (apps/)
Specialized domain logic per use case:
- **Domain schemas:** What data to extract
- **Custom prompts:** Industry-specific language
- **Output formats:** Memos, reports, assessments

### Platform Layer (libs/agentkit)
Shared infrastructure for rapid development:
- **infra/:** Config, logging, decorators
- **services/:** LLM, search, extraction, vector store
- **testing/:** Mock fixtures for fast tests
- **patterns/:** Copy-paste LangGraph templates

## Success Metrics

### Quality
| Metric | Target |
|--------|--------|
| **Output Coherence** | Structured, cited, actionable |
| **Critique Effectiveness** | >50% of outputs improve after critic pass |
| **Test Coverage** | >80% across all packages |

### Velocity
| Metric | Target |
|--------|--------|
| **New App Bootstrap** | <1 day using agentkit |
| **Shared Code Ratio** | >80% infrastructure in libs/ |
| **Iteration Speed** | Changes deploy in minutes |
