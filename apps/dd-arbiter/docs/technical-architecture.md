# Technical Architecture: Multi-Model Adversarial Research System

**Version:** 1.0
**Last Updated:** December 27, 2024

---

## Overview

The Due Diligence Arbiter implements a 5-layer architecture for adversarial multi-model research with uncertainty quantification. The core insight: **model disagreement is signal, not noise**.

```
┌─────────────────────────────────────────────────────────────┐
│                    SYSTEM ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│ LAYER 1: Routing                                             │
│   • LiteLLM proxy (handles OpenAI, Anthropic, Google)       │
│   • GPTCache semantic layer (Redis + sentence-transformers) │
│   • Complexity classifier (simple prompt → skip ensemble)    │
├─────────────────────────────────────────────────────────────┤
│ LAYER 2: Parallel Execution                                  │
│   • LangGraph StateGraph with fan-out edges                 │
│   • 3 models: GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro    │
│   • Async execution via asyncio.gather()                    │
├─────────────────────────────────────────────────────────────┤
│ LAYER 3: Uncertainty                                         │
│   • Self-consistency: 10 samples per model for complex Qs   │
│   • Semantic clustering: DeBERTa-Large-MNLI                 │
│   • Entropy computation: cluster-frequency based            │
├─────────────────────────────────────────────────────────────┤
│ LAYER 4: Disagreement                                        │
│   • Claim extraction via LLM prompting                      │
│   • Pairwise NLI comparison                                 │
│   • Contradiction surfacing with model attribution          │
├─────────────────────────────────────────────────────────────┤
│ LAYER 5: Synthesis                                           │
│   • Arbiter model (GPT-4o or Claude)                        │
│   • Structured output via Instructor + Pydantic             │
│   • Conditional critic (low confidence only)                │
├─────────────────────────────────────────────────────────────┤
│ OBSERVABILITY                                                │
│   • Langfuse or Helicone for tracing                        │
│   • Cost tracking per query                                 │
│   • Cache hit rate monitoring                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Query Routing and Caching

### Purpose

Before hitting any model, queries pass through routing logic to optimize cost and latency.

### Components

**Semantic Cache (GPTCache)**
- Returns cached results for semantically similar questions
- Uses embedding similarity threshold (0.95 recommended)
- Expected hit rates: 18-60% in Q&A scenarios

**Complexity Router**
- Simple factual lookups → single fast model
- Complex research questions → full ensemble
- Decision based on query characteristics (length, ambiguity, stakes)

### Implementation

```python
from gptcache import cache
from gptcache.embedding import Onnx
from gptcache.similarity_evaluation import OnnxModelEvaluation

# Initialize semantic cache
cache.init(
    embedding_func=Onnx(),
    similarity_evaluation=OnnxModelEvaluation(),
    similarity_threshold=0.95
)

def route_query(query: str) -> str:
    """Determine if query needs multi-model or single model."""
    # Heuristics for complexity
    is_complex = (
        len(query) > 200 or
        any(word in query.lower() for word in ["analyze", "compare", "evaluate", "assess"]) or
        "investment" in query.lower()
    )
    return "ensemble" if is_complex else "single"
```

---

## Layer 2: Parallel Independent Generation

### Purpose

Execute multiple models simultaneously with no cross-contamination. True independence is critical for meaningful disagreement detection.

### Key Principle

The Mixture of Agents paper proved models improve when given other models' outputs. But for **disagreement detection**, we need genuine independence first. Cross-pollination happens in synthesis, not generation.

### Implementation

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator
import asyncio

class ResearchState(TypedDict):
    query: str
    document_content: str  # Parsed CIM content
    model_responses: Annotated[list[dict], operator.add]
    clusters: list[dict]
    disagreements: list[dict]
    final_answer: dict

async def research_with_model(
    state: ResearchState,
    model_name: str,
    client,
    role: str = "analyst"
) -> dict:
    """Execute research with a single model in a specific role."""

    role_prompts = {
        "bull": "You are a bullish investment analyst. Build the strongest possible case for this investment.",
        "bear": "You are a skeptical analyst. Identify every weakness, risk, and reason this deal could fail.",
        "analyst": "You are a neutral analyst. Provide balanced analysis of this opportunity."
    }

    system_prompt = role_prompts.get(role, role_prompts["analyst"])

    response = await client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this CIM:\n\n{state['document_content']}"}
        ],
        temperature=0.7
    )

    return {
        "model_responses": [{
            "model": model_name,
            "role": role,
            "response": response.choices[0].message.content,
        }]
    }

# Build parallel execution graph
builder = StateGraph(ResearchState)

# Add nodes for each model
builder.add_node("gpt4_bull", lambda s: research_with_model(s, "gpt-4o", openai_client, "bull"))
builder.add_node("claude_bear", lambda s: research_with_model(s, "claude-3-5-sonnet-20241022", anthropic_client, "bear"))
builder.add_node("gemini_analyst", lambda s: research_with_model(s, "gemini-1.5-pro", google_client, "analyst"))

# Fan-out: all models execute in parallel
builder.add_edge(START, "gpt4_bull")
builder.add_edge(START, "claude_bear")
builder.add_edge(START, "gemini_analyst")

# Fan-in: wait for all, then cluster
builder.add_edge(["gpt4_bull", "claude_bear", "gemini_analyst"], "cluster")
```

### Preventing Anchoring Bias

Research (arXiv:2412.06593) found simple strategies like "ignore previous context" are insufficient. For genuine independence:

1. **No cross-model context** in generation phase
2. **Anonymized references** during peer review ("Response A" not "GPT-4 said")
3. **Both-Anchor technique** if reference info needed: include contradictory reference points

---

## Layer 3: Uncertainty Quantification

### Purpose

Produce calibrated confidence scores without access to model logprobs.

### Core Method: Semantic Entropy

For black-box models (Claude, GPT-4), **semantic entropy combined with self-consistency** provides the most reliable uncertainty signal.

**Algorithm:**
1. Generate 5-10 responses at temperature 0.7-1.0
2. Cluster responses using bidirectional NLI entailment
3. Compute cluster-frequency entropy: `SE = -Σ (count_c/N) log(count_c/N)`
4. High SE = uncertain (many semantic clusters)
5. Low SE = confident (one dominant cluster)

### The Verbalized Confidence Trap

Asking models "how confident are you (0-100%)?" produces systematically overconfident estimates. Research (ICLR 2024) found **84%+ of scenarios show overconfidence**.

**Mitigation:** Weight verbalized confidence lower than consistency-based measures.

### Implementation

```python
from collections import Counter
from math import log
from pydantic import BaseModel
from transformers import pipeline

class UncertaintyResult(BaseModel):
    answer: str
    confidence: float
    semantic_entropy: float
    consistency_score: float
    num_semantic_clusters: int
    verbalized_confidence_avg: float

# Load NLI model for clustering
nli = pipeline("zero-shot-classification", model="microsoft/deberta-large-mnli")

def semantic_cluster_nli(responses: list[str]) -> list[dict]:
    """Cluster responses by semantic equivalence using NLI."""
    clusters = []

    for resp in responses:
        matched = False
        for cluster in clusters:
            # Bidirectional entailment check
            forward = nli(resp, [cluster["representative"]])["scores"][0]
            backward = nli(cluster["representative"], [resp])["scores"][0]

            if forward > 0.7 and backward > 0.7:
                cluster["members"].append(resp)
                cluster["count"] += 1
                matched = True
                break

        if not matched:
            clusters.append({
                "representative": resp,
                "members": [resp],
                "count": 1,
                "cluster_id": len(clusters)
            })

    return clusters

def compute_uncertainty(
    prompt: str,
    model_client,
    n_samples: int = 10,
    temperature: float = 0.7
) -> UncertaintyResult:
    """Compute comprehensive uncertainty without logprobs."""

    # Generate diverse samples
    responses = []
    verbalized_confidences = []

    confidence_prompt = f"""{prompt}

After your answer, on a new line write "Confidence: X%" where X is 0-100."""

    for _ in range(n_samples):
        result = model_client.generate(confidence_prompt, temperature=temperature)
        answer, conf = parse_answer_and_confidence(result)
        responses.append(answer)
        verbalized_confidences.append(conf)

    # Semantic clustering via NLI
    clusters = semantic_cluster_nli(responses)

    # Compute metrics
    total = sum(c["count"] for c in clusters)

    # Consistency = frequency of most common cluster
    consistency = max(c["count"] for c in clusters) / total

    # Semantic entropy
    probs = [c["count"] / total for c in clusters]
    semantic_entropy = -sum(p * log(p) for p in probs if p > 0)

    # Weighted combination (consistency weighted higher)
    confidence_variance = variance(verbalized_confidences)
    if confidence_variance < 0.1:  # High agreement
        final_confidence = 0.7 * consistency + 0.3 * mean(verbalized_confidences) / 100
    else:  # Disagreement - rely on consistency
        final_confidence = 0.85 * consistency + 0.15 * mean(verbalized_confidences) / 100

    return UncertaintyResult(
        answer=clusters[0]["representative"],  # Most common
        confidence=final_confidence,
        semantic_entropy=semantic_entropy,
        consistency_score=consistency,
        num_semantic_clusters=len(clusters),
        verbalized_confidence_avg=mean(verbalized_confidences)
    )
```

---

## Layer 4: Disagreement Detection

### Purpose

Identify specific claims where models diverge—the actionable insight for human review.

### Surface vs Substantive Disagreement

| Type | Example | Signal Value |
|------|---------|--------------|
| Surface | "Paris" vs "The capital is Paris" | Noise |
| Substantive | "Revenue grew 15%" vs "Revenue declined 3%" | High signal |

The distinction requires semantic analysis, not string matching.

### Implementation

```python
def extract_claims(response: str) -> list[str]:
    """Extract atomic factual claims from a response."""
    extraction_prompt = f"""List each factual claim in this text as a separate bullet:

{response}

Format: One claim per line, starting with "- "
Focus on:
- Numerical claims (revenue, growth, margins)
- Directional claims (increasing, declining)
- Categorical claims (market leader, competitor)
- Risk assessments
"""
    # Call LLM for extraction
    result = llm.generate(extraction_prompt)
    return [line.strip("- ").strip() for line in result.split("\n") if line.strip().startswith("-")]

def check_claim_relationship(claim_a: str, claim_b: str) -> str:
    """Determine if two claims agree, contradict, or are unrelated."""

    # Forward entailment check
    entailment = nli(claim_a, candidate_labels=[claim_b])

    if entailment['scores'][0] > 0.7:
        return "agreement"

    # Contradiction check
    negated = f"It is not the case that {claim_b}"
    contradiction = nli(claim_a, candidate_labels=[negated])

    if contradiction['scores'][0] > 0.7:
        return "contradiction"

    return "unrelated"

def detect_disagreements(state: ResearchState) -> dict:
    """Find contradicting claims across model responses."""

    # Extract claims from each response
    all_claims = {}
    for resp in state["model_responses"]:
        claims = extract_claims(resp["response"])
        all_claims[resp["model"]] = {
            "role": resp["role"],
            "claims": claims
        }

    # Pairwise comparison
    disagreements = []
    models = list(all_claims.keys())

    for i, m1 in enumerate(models):
        for m2 in models[i+1:]:
            for c1 in all_claims[m1]["claims"]:
                for c2 in all_claims[m2]["claims"]:
                    relationship = check_claim_relationship(c1, c2)

                    if relationship == "contradiction":
                        disagreements.append({
                            "claim_1": {
                                "model": m1,
                                "role": all_claims[m1]["role"],
                                "claim": c1
                            },
                            "claim_2": {
                                "model": m2,
                                "role": all_claims[m2]["role"],
                                "claim": c2
                            },
                            "type": "contradiction",
                            "severity": assess_severity(c1, c2)
                        })

    return {"disagreements": disagreements}

def assess_severity(claim_1: str, claim_2: str) -> str:
    """Assess how deal-breaking a disagreement is."""
    high_stakes_keywords = ["revenue", "growth", "decline", "loss", "risk", "regulatory", "legal"]

    combined = (claim_1 + claim_2).lower()
    matches = sum(1 for kw in high_stakes_keywords if kw in combined)

    if matches >= 2:
        return "high"
    elif matches >= 1:
        return "medium"
    return "low"
```

---

## Layer 5: Adversarial Synthesis

### Purpose

Combine all model outputs into a structured report with clear agreement/disagreement sections.

### The Self-Critique Paradox

Adversarial critique **helps on hard tasks but harms on easy ones** (Snorkel AI research). When a model is already confident and correct, critics will invent problems.

**Solution:** Engage critics conditionally based on uncertainty scores.

```python
def should_engage_critic(state: ResearchState) -> bool:
    """Decide if adversarial critique adds value."""

    # High disagreement → engage critic
    if len(state["disagreements"]) > 3:
        return True

    # Low confidence → engage critic
    if state.get("confidence_score", 1.0) < 0.6:
        return True

    # High confidence + consensus → skip critic
    return False
```

### Structured Output Schema

```python
from pydantic import BaseModel, Field
from typing import List

class Claim(BaseModel):
    text: str = Field(description="The specific factual claim")
    confidence: float = Field(ge=0, le=1, description="Confidence 0-1")
    supporting_models: List[str] = Field(description="Models that agree")
    contradicting_models: List[str] = Field(description="Models that disagree")

class DiligenceReport(BaseModel):
    """Structured output for CIM analysis."""

    # Summary
    thesis_confidence_score: float = Field(
        ge=0, le=100,
        description="Overall confidence in the investment thesis (0-100)"
    )
    executive_summary: str = Field(description="2-3 sentence summary")

    # Consensus findings
    consensus_claims: List[Claim] = Field(
        description="Claims all models agree on"
    )

    # Disputed findings (the value-add)
    disputed_claims: List[Claim] = Field(
        description="Claims where models disagree"
    )

    # Risk assessment
    key_risks: List[str] = Field(description="Top risks identified")
    deal_breakers: List[str] = Field(description="Potential deal-killing issues")

    # Action items
    diligence_questions: List[str] = Field(
        description="Suggested questions for management/advisors"
    )

    # Meta
    needs_human_review: bool = Field(
        description="True if high uncertainty or major disagreements"
    )
    review_reason: str | None = Field(
        default=None,
        description="Why human review is recommended"
    )
```

### Synthesis Implementation

```python
import instructor
from openai import OpenAI

# Patch client for structured output
client = instructor.from_openai(OpenAI())

def synthesize_report(state: ResearchState) -> DiligenceReport:
    """Generate structured diligence report from all inputs."""

    synthesis_prompt = f"""You are synthesizing investment research from multiple AI models analyzing a CIM.

ORIGINAL QUERY: {state["query"]}

MODEL RESPONSES:
{format_responses(state["model_responses"])}

DETECTED DISAGREEMENTS:
{format_disagreements(state["disagreements"])}

NUMBER OF SEMANTIC CLUSTERS: {len(state["clusters"])}

Your task:
1. Identify claims where ALL models agree (high confidence)
2. Highlight claims where models DISAGREE (requires human verification)
3. Assess overall thesis confidence based on:
   - Strength of bull case
   - Validity of bear critiques
   - Resolution of disagreements
4. Generate specific diligence questions for unresolved issues
5. Flag if human review is needed (high-stakes disagreements)
"""

    return client.chat.completions.create(
        model="gpt-4o",
        response_model=DiligenceReport,
        messages=[{"role": "user", "content": synthesis_prompt}],
        max_retries=2
    )
```

---

## Data Flow

```
CIM Upload
    ↓
[PDF Parser] → Extract text, tables, key metrics
    ↓
[Semantic Cache Check]
    ↓ (cache miss)
[Complexity Router] → Simple: Single model path
    ↓ (complex)
[Parallel Execution]
    ├─→ GPT-4o (Bull role)
    ├─→ Claude 3.5 (Bear role)
    └─→ Gemini 1.5 (Analyst role)
    ↓
[Semantic Clustering] → Compute uncertainty
    ↓
[Claim Extraction + NLI]
    ↓
[Disagreement Detection]
    ↓
[Conditional Critic] → Only if low confidence
    ↓
[Arbiter Synthesis] → Structured DiligenceReport
    ↓
[Final Output]
```

---

## Performance Characteristics

| Metric | Expected Value |
|--------|----------------|
| **Latency (cached)** | 2-5 seconds |
| **Latency (full ensemble)** | 15-30 seconds |
| **Cost multiplier** | 3-4x single model |
| **Cost with caching** | ~1.5x single model |
| **Cache hit rate** | 20-40% |
| **Accuracy improvement** | 15-25% reduction in hallucinations |

---

## Essential Repositories

| Repository | Purpose |
|------------|---------|
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | Graph orchestration |
| [jxnl/instructor](https://github.com/jxnl/instructor) | Structured outputs |
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | Multi-provider routing |
| [zilliztech/GPTCache](https://github.com/zilliztech/GPTCache) | Semantic caching |
| [jlko/semantic_uncertainty](https://github.com/jlko/semantic_uncertainty) | Semantic entropy |

---

## Essential Papers

| Paper | Key Insight |
|-------|-------------|
| Wang et al., "Mixture-of-Agents" | Models improve with other models' outputs |
| Kuhn et al., "Semantic Entropy" (Nature 2024) | Gold standard for black-box uncertainty |
| Xiong et al., "Can LLMs Express Uncertainty?" | Verbalized confidence is systematically wrong |
| Farquhar et al., "Detecting Hallucinations" | Claim-level detection via semantic entropy |

---

## Key Architectural Decisions

### Start with 3 models, not more

Diminishing returns kick in quickly. GPT-4o + Claude 3.5 + Gemini 1.5 provides sufficient diversity.

### Use semantic entropy, not verbalized confidence

LLMs are systematically overconfident. Consistency-based measures are more reliable.

### Only engage critics selectively

The self-critique paradox is real. Gate critic engagement on uncertainty scores.

### Cache aggressively

Research queries often repeat or paraphrase. 30% cache hit rate cuts costs nearly in half.

### Schema enforcement is non-negotiable

Different models produce wildly different structures. Instructor + Pydantic eliminates this chaos.
