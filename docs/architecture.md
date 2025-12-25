# Architecture

This document explains the technical architecture of FounderMode, including its multi-agent workflow, memory system, and design decisions.

## System Overview

FounderMode is built on a **stateful, cyclic multi-agent architecture** using LangGraph. The system processes a business idea through four specialized agents that collaborate to produce investment-grade analysis.

```
                    ┌──────────────────────────────────────────────┐
                    │            FounderMode System                │
                    └──────────────────────────────────────────────┘
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         │                               │                               │
         ▼                               ▼                               ▼
┌─────────────────┐            ┌─────────────────┐            ┌─────────────────┐
│   Graph Layer   │            │   Tools Layer   │            │  Memory Layer   │
│   (LangGraph)   │◀──────────▶│  (Search/Scrape)│◀──────────▶│   (ChromaDB)    │
└─────────────────┘            └─────────────────┘            └─────────────────┘
         │
         ▼
┌─────────────────┐
│   API Layer     │
│  (CLI/FastAPI)  │
└─────────────────┘
```

## Core Workflow

### The Agent Loop

The system implements a **Planner → Researcher → Writer → Critic** workflow with feedback loops:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          WORKFLOW GRAPH                                   │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│    START                                                                 │
│      │                                                                   │
│      ▼                                                                   │
│  ┌────────┐    ┌──────────────┐    ┌────────┐    ┌────────┐            │
│  │Planner │───▶│  Researcher  │───▶│ Writer │───▶│ Critic │            │
│  └───┬────┘    └──────────────┘    └────────┘    └───┬────┘            │
│      │               ▲                               │                   │
│      │               │         Rejection Loop        │                   │
│      │               └───────────────────────────────┘                   │
│      │                                               │                   │
│      │              ┌────────────────────────────────┘                   │
│      │              │ Approval                                           │
│      ▼              ▼                                                    │
│  [Decide]        [END]                                                   │
│   │    │                                                                 │
│   │    └──────────▶ Writer (if enough facts)                            │
│   └────────────────▶ Researcher (if more research needed)               │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Agent Responsibilities

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **Planner** | Strategic Director | Facts + Critique | Next research topic OR "write" signal |
| **Researcher** | Data Gatherer | Research topic | List of verified facts |
| **Writer** | Analyst | All facts | Structured Investment Memo |
| **Critic** | Managing Partner | Memo + Facts | Approve OR Reject with feedback |

## State Management

### FounderState

The workflow maintains state through a `TypedDict` that flows between agents:

```python
class FounderState(TypedDict):
    # User input
    research_question: str          # Original business idea

    # Research accumulation
    research_facts: List[ResearchFact]  # Grows via merge operator
    research_topic: str             # Current focus area

    # Output
    memo_draft: InvestmentMemo      # Latest memo version

    # Control flow
    next_step: str                  # "research" | "write" | "reject" | "approve"
    critique_history: List[str]    # Feedback from Critic
    revision_count: int             # Loop counter (max 3)

    # Context
    messages: List[BaseMessage]     # Chat history
```

### State Flow

```
1. User Input ──▶ research_question populated
2. Planner    ──▶ Sets research_topic, next_step
3. Researcher ──▶ Appends to research_facts
4. Writer     ──▶ Sets memo_draft
5. Critic     ──▶ Sets next_step (approve/reject), updates critique_history
6. Loop       ──▶ revision_count increments on rejection
```

## Agent Deep Dive

### Planner Agent

**Purpose:** Decides what to research next or when to write.

**Prompt Persona:** Senior Investment Strategist

**Logic:**
1. Reviews gathered facts
2. Considers any critique feedback
3. Identifies gaps in analysis
4. Either assigns next research topic OR signals "write"

**Constraints:**
- Maximum 20 facts before forcing write phase
- Prevents infinite research loops

### Researcher Agent

**Purpose:** Gathers factual data from the web.

**Process:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    RESEARCHER PIPELINE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. SEARCH                                                      │
│     └── Tavily API ──▶ Returns snippets + URLs                 │
│                                                                 │
│  2. URL SELECTION                                               │
│     └── LLM selects 1-3 high-value URLs for deep scraping      │
│                                                                 │
│  3. DEEP SCRAPING                                               │
│     └── For each selected URL:                                  │
│         ├── Playwright (JS rendering if needed)                │
│         ├── Readability (main content extraction)              │
│         └── BeautifulSoup (fallback text extraction)           │
│                                                                 │
│  4. FACT EXTRACTION                                             │
│     └── LLM extracts structured facts with sources             │
│                                                                 │
│  5. MEMORY STORAGE                                              │
│     └── Facts stored in ChromaDB for deduplication             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Output:** List of `ResearchFact` objects with:
- Claim text
- Source URL
- Relevance score
- Extraction timestamp

### Writer Agent

**Purpose:** Synthesizes facts into Investment Memo.

**Prompt Persona:** Partner at Sequoia Capital

**Output Structure:**
```
InvestmentMemo
├── executive_summary: str    # BLUF + opportunity assessment
├── market_analysis: str      # TAM/SAM/SOM, trends, dynamics
└── competitive_landscape: str # Competitors, moats, risks
```

**Citation Rules:**
- Every quantitative claim must have a citation
- Format: "Claim text [Source: URL]"
- No unattributed statistics

### Critic Agent

**Purpose:** Adversarial quality review.

**Prompt Persona:** Skeptical Managing Partner

**Evaluation Criteria:**
1. **Quantitative Rigor** - CAC, LTV, Churn, TAM numbers present?
2. **Citation Quality** - Claims backed by research log?
3. **Analytical Depth** - Concrete risks identified?
4. **Objectivity** - Balanced view, not promotional?

**Actions:**
- **APPROVE** → Workflow ends, memo published
- **REJECT** → Specific feedback provided, loops back to Planner

**Safeguards:**
- Maximum 3 revision iterations
- Auto-approves after max iterations to prevent infinite loops

## Memory System

### ChromaDB Integration

FounderMode uses a vector database for semantic memory:

```
┌──────────────────────────────────────────────────────────────┐
│                    MEMORY ARCHITECTURE                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────┐                                          │
│  │ Research Fact  │                                          │
│  │ "Company X     │                                          │
│  │  raised $50M"  │                                          │
│  └───────┬────────┘                                          │
│          │                                                   │
│          ▼                                                   │
│  ┌────────────────┐     ┌────────────────┐                  │
│  │   Chunking     │────▶│   Embedding    │                  │
│  │ (1000 chars)   │     │ (OpenAI ada)   │                  │
│  └────────────────┘     └───────┬────────┘                  │
│                                 │                            │
│                                 ▼                            │
│                    ┌────────────────────┐                   │
│                    │     ChromaDB       │                   │
│                    │  Vector Storage    │                   │
│                    │  (Persistent)      │                   │
│                    └────────────────────┘                   │
│                                                              │
│  QUERIES:                                                    │
│  • Deduplication (before searching)                          │
│  • Context retrieval (for writing)                           │
│  • Semantic similarity search                                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Benefits

1. **Deduplication:** Won't search for facts already known
2. **Context Window:** Retrieves relevant past research
3. **Persistence:** Knowledge survives across sessions
4. **Semantic Search:** Finds related facts by meaning, not keywords

## Tools Layer

### TavilySearch

Web search with semantic caching:

```python
# Workflow
1. Check ChromaDB for similar queries
2. If cache miss → Call Tavily API
3. Store results in ChromaDB
4. Return structured search results
```

### Deep Scraper

Multi-stage content extraction:

```
Stage 1: Playwright (optional)
    └── Renders JavaScript-heavy pages

Stage 2: Readability-lxml
    └── Extracts main article content

Stage 3: BeautifulSoup
    └── Fallback text extraction

Output: Clean text content
```

## Human-in-the-Loop

FounderMode pauses before the Researcher agent executes:

```
┌─────────┐    ┌──────────────────┐    ┌────────────┐
│ Planner │───▶│   INTERRUPT      │───▶│ Researcher │
└─────────┘    │ (User Approval)  │    └────────────┘
               └──────────────────┘
```

**Interactive Mode:**
- Shows planned search query
- Asks for confirmation
- User can modify or skip

**Auto Mode:**
- Bypasses interrupt
- Fully autonomous operation

## Design Decisions

### Why Cyclic Graphs?

Traditional linear pipelines can't self-correct. The Critic loop enables:
- Iterative refinement
- Quality enforcement
- Recovery from incomplete research

### Why Vector Memory?

In-memory storage forgets between sessions. ChromaDB provides:
- Persistent knowledge
- Semantic deduplication
- Efficient context retrieval

### Why Multi-Stage Scraping?

Single-method scraping fails on many sites. The pipeline handles:
- JavaScript-rendered content (Playwright)
- Article extraction (Readability)
- Raw HTML parsing (BeautifulSoup)

### Why Human-in-the-Loop?

Autonomous agents can go off-track. HITL provides:
- User oversight
- Course correction
- Trust building

## Diagrams

For visual representations, see:

- [System Overview](./diagrams/system-overview.puml) - High-level architecture
- [Workflow Sequence](./diagrams/workflow-sequence.puml) - Agent interactions
- [Component Diagram](./diagrams/components.puml) - Module dependencies
- [State Machine](./diagrams/state-machine.puml) - Workflow states

---

[← Back to Documentation Index](./README.md)
