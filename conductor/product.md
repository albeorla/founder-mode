# Product Guide: Deal-Screener (Powered by Founder-Mode Engine)

## Vision
**"The 24/7 Private Equity Associate"**

Deal-Screener is an autonomous diligence agent that pre-screens data rooms before a human investor ever opens a file. It is the flagship product built on the **Founder-Mode Engine** (a monorepo venture studio platform).

Unlike generic AI wrappers that chat with PDFs, Deal-Screener uses a purpose-built **Cyclic Multi-Agent Graph** to read, cross-reference, and adversarially critique the private data in an M&A data room.

## Core Value Proposition

### 1. The "Red Flag" Filter
PE Associates spend 80% of their time scrubbing data rooms for basic discrepancies and only 20% on strategic thinking. Deal-Screener inverts this.
- **Input:** Data Room URL (PDFs, Excel models, contracts) + Investment Thesis (e.g., "B2B SaaS, <5% churn, >$5M ARR").
- **Action:** Reads every document, calculates metrics from raw data, and cross-checks them.
- **Output:** A "Red Flag Report" and a Draft Investment Committee (IC) Memo.

### 2. The Data Moat
- **Private Data > Public Search:** We process proprietary data (financials, contracts) that Google/Perplexity cannot access.
- **High Switching Costs:** Once a firm integrates their data room provider (Intralinks, Datasite) with us, the friction to switch is massive.

### 3. The "Critic" Advantage
The architecture leverages an **Adversarial Critic Node**. In Private Equity, you *want* a skeptic.
- *Standard AI:* "Revenue grew 20% YoY."
- *Deal-Screener:* "Reject. The Excel model shows 20% growth, but the bank statements in PDF only support 12%. Flagging for potential fraud."

## Architecture Layers

### Product Layer (Deal-Screener)
The specialized logic for M&A diligence:
- **Scanner Agent:** Extracts numbers from unstructured PDFs and structured CSVs.
- **Analyst Agent:** Calculates key metrics (CAC, LTV, EBITDA adjustments).
- **Critic Agent:** Checks for inconsistencies between documents.

### Platform Layer (Founder-Mode Engine / AgentKit)
The shared infrastructure enabling rapid agent development:
- **libs/agentkit:** Reusable components for LLM management, structured logging, and retry logic.
- **State Management:** LangGraph-based state machines.
- **Vector Memory:** Semantic search for deduping claims.

## Success Metrics

### Product Performance
| Metric | Target |
|--------|--------|
| **Recall** | >95% of "Red Flags" identified by human associates |
| **Precision** | <10% false positive rate on discrepancies |
| **Time-to-Memo** | <15 minutes per deal (vs. 4-8 hours human time) |

### Business Traction
| Metric | Target |
|--------|--------|
| **Pilots** | 5 PE Firms piloted in Q1 |
| **Integrations** | 1 Data Room Provider (e.g., Intralinks) |
| **Defensibility** | "Critic" model fine-tuned on 100+ historical fraud cases |

## Roadmap
- **Phase 1 (Complete):** Engine Migration & AgentKit.
- **Phase 2 (Current):** Strategic Pivot & Documentation.
- **Phase 3:** AgentKit Expansion (Data Room Connectors).
- **Phase 4:** Deal-Screener MVP.
