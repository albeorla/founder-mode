# Product Guide: FounderMode (The Autonomous Due Diligence Agent)

## Vision
FounderMode is an autonomous market research agent that validates business ideas end-to-end. Unlike simple wrapper tools, it employs a **multi-agent architecture** to simulate a human investment analyst: reading data, forming hypotheses, and actively verifying facts via web search.

## Core Value Proposition
- **Active Reasoning:** It doesn't just summarize; it actively validates claims by searching the web.
- **Deep Reports:** Generates strategic investment memos (10+ pages) from a single one-sentence prompt.
- **Agentic Architecture:** Uses cyclic graphs to self-correct (e.g., "I couldn't find pricing, I'll look again").

## Target Users
- **Founders:** Pre-deck validation ("Is this idea stupid?").
- **VC Associates:** Automated screening of inbound startups.
- **Corporate Strategy:** Rapid market sizing and competitor analysis.

## Key Features
- **Vector-Native Memory:** Uses embeddings (ChromaDB) to deduplicate and cluster semantically.
- **Research Agent:** A dedicated agent that uses tools (Tavily) to fact-check assumptions.
- **Strategic Synthesis:** Merges "User Pain" (social signals) with "Market Reality" (competitor data).
- **Human-in-the-Loop:** Allows users to review and refine research plans before execution.
- **Polished Artifacts:** Automatically generates professional HTML reports from synthesized memos.
