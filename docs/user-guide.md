# User Guide

This guide covers all the ways to use FounderMode, including advanced options, best practices, and troubleshooting.

## Command Reference

### Basic Usage

**Using Docker (Recommended):**
```bash
docker compose run --rm app run "Your business idea description"
```

**Using Local Installation:**
```bash
foundermode run "Your business idea description"
```

### Options

| Flag | Short | Description |
|------|-------|-------------|
| `--auto` | `-a` | Skip human approval prompts (fully autonomous) |
| `--help` | `-h` | Show help message |

### Examples

**Docker:**
```bash
# Interactive mode (default) - pauses for approval
docker compose run --rm app run "A B2B SaaS platform for construction project management"

# Auto mode - no human interaction required
docker compose run --rm app run --auto "An AI tutoring app for K-12 students"
```

**Local:**
```bash
# Interactive mode (default) - pauses for approval
foundermode run "A B2B SaaS platform for construction project management"

# Auto mode - no human interaction required
foundermode run --auto "An AI tutoring app for K-12 students"

# Short flag
foundermode run -a "Subscription box service for specialty coffee"
```

## REST API

FounderMode also provides a REST API for programmatic access.

### Starting the Server

**Using Docker (Recommended):**
```bash
# Start the API server (runs on port 8000)
docker compose up

# Or run in background
docker compose up -d
```

**Using Local Installation:**
```bash
uvicorn foundermode.api.server:app --host 0.0.0.0 --port 8000
```

API docs available at: `http://localhost:8000/docs`

### Endpoints

#### Start a New Analysis

```bash
POST /run
Content-Type: application/json

{
  "idea": "Your business idea here"
}
```

**Response:**
```json
{
  "run_id": "uuid-string",
  "status": "running"
}
```

#### Check Status

```bash
GET /run/{run_id}
```

**Response:**
```json
{
  "run_id": "uuid-string",
  "status": "completed",
  "memo": { ... }
}
```

#### Health Check

```bash
GET /health
```

## Interactive Mode Deep Dive

### Approval Prompts

In interactive mode, FounderMode pauses before each research step:

```
[Planner] Research focus: "enterprise construction software market size"

>>> Researcher wants to search for: enterprise construction software market size
>>> Continue? [Y/n]:
```

**Options:**
- **Y** (or Enter): Proceed with the search
- **n**: Skip this search and let Planner choose another topic

### When to Use Interactive Mode

- **Exploring unfamiliar markets** - You can guide research direction
- **Sensitive topics** - Review queries before they're executed
- **Learning the system** - See how FounderMode thinks
- **Debugging** - Understand why analysis went a certain direction

### When to Use Auto Mode

- **Batch processing** - Running multiple analyses
- **CI/CD pipelines** - Automated research workflows
- **Trusted topics** - Well-understood market spaces
- **Time-constrained** - Need results without babysitting

## Crafting Effective Prompts

### Good Prompts

Specific and clear prompts yield better results:

```bash
# Good: Specific market and model
foundermode run "A SaaS platform helping e-commerce brands manage returns, charging per transaction"

# Good: Clear target customer
foundermode run "B2B software for mid-market HR teams to automate employee onboarding"

# Good: Specific technology angle
foundermode run "Using computer vision to detect manufacturing defects in semiconductor fabs"
```

### Weak Prompts

Vague prompts lead to generic analysis:

```bash
# Weak: Too vague
foundermode run "An app for people"

# Weak: No business model
foundermode run "AI stuff"

# Weak: Too broad
foundermode run "A company that does things"
```

### Prompt Components

The best prompts include:

1. **Target Customer**: Who will pay?
2. **Problem Solved**: What pain point?
3. **Solution Type**: Software, hardware, service?
4. **Business Model**: How do you make money?

**Template:**
```
"A [solution type] for [target customer] to [solve problem], monetized via [business model]"
```

## Understanding the Output

### Investment Memo Structure

The output HTML contains three sections:

#### 1. Executive Summary

- **BLUF** (Bottom Line Up Front): Investment recommendation
- **Opportunity Assessment**: Market opportunity summary
- **Key Metrics**: Critical numbers at a glance

#### 2. Market Analysis

- **TAM/SAM/SOM**: Market sizing with sources
- **Market Trends**: Growth drivers and headwinds
- **Customer Segments**: Who buys and why

#### 3. Competitive Landscape

- **Direct Competitors**: Head-to-head competition
- **Adjacent Players**: Potential future competition
- **Competitive Moats**: Defensibility analysis
- **Risks**: Specific concerns and mitigations

### Citations

Every quantitative claim includes a citation:

```
The global construction software market reached $10.2B in 2023
[Source: https://www.grandviewresearch.com/...]
```

**No citation = claim wasn't verified.** If you see uncited claims, the system may need additional research cycles.

### Quality Indicators

**Strong Analysis:**
- Specific numbers (not "large market" but "$4.2B TAM")
- Multiple competitor profiles with pricing
- Concrete risks (not "competition" but "Salesforce entering via acquisition")
- Clear recommendation with reasoning

**Weak Analysis (triggers Critic rejection):**
- Vague qualitative statements
- Missing financial metrics
- No competitor specifics
- Promotional tone without evidence

## Memory and Caching

### How Memory Works

FounderMode remembers previous research:

1. **Search Caching**: Repeated queries return cached results
2. **Fact Deduplication**: Won't re-research known facts
3. **Context Retrieval**: Related research informs new queries

### Memory Location

By default, memory is stored in `.chroma_db/` in your working directory.

```bash
# Check memory location
ls -la .chroma_db/

# Clear memory (start fresh)
rm -rf .chroma_db/
```

### When to Clear Memory

Clear memory when:
- Starting research on a completely new topic
- Previous research may have outdated information
- You want a "clean slate" analysis

Keep memory when:
- Researching related topics
- Doing iterative refinement
- Building knowledge over time

## Troubleshooting

### Common Issues

#### "Could not find any results"

The Tavily search didn't return useful data. Try:
- Rephrasing your business idea
- Using more specific industry terms
- Checking your Tavily API key

#### "Mock data detected"

The system is running without live API keys. Check:
```bash
echo $OPENAI_API_KEY
echo $TAVILY_API_KEY
```

#### Critic Keeps Rejecting

If the Critic rejects repeatedly:
- Your idea may need clearer definition
- The market may lack public data
- Try a more established market for testing

After 3 rejections, the system auto-approves to prevent infinite loops.

#### Slow Performance

Deep scraping takes time. To diagnose:
```bash
export FM_LOG_LEVEL=DEBUG
foundermode run "your idea"
```

This shows detailed progress including:
- Which URLs are being scraped
- How long each step takes
- Any retry attempts

### Docker-Specific Issues

#### Container can't access API keys

Ensure your `.env` file is properly configured:
```bash
# Check file exists and has content
ls -la .env
```

The `.env` file should contain:
```env
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

#### Playwright/Chromium errors in container

If you see browser errors inside Docker, rebuild the container:
```bash
docker compose build --no-cache
```

#### Container tests for validation

Run the container integration tests to verify everything works:
```bash
docker compose run --rm app pytest tests/container/
```

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `APIKeyError` | Missing/invalid API key | Set environment variables |
| `RateLimitError` | Too many API calls | Wait and retry, or upgrade API tier |
| `TimeoutError` | Web scraping timeout | Retry; some sites are slow |
| `ConnectionError` | Network issues | Check internet connection |

## Best Practices

### For Founders

1. **Start broad, then narrow**: First run with general idea, then refine based on results
2. **Validate surprising claims**: If a number seems off, search manually
3. **Use for ideation**: Generate multiple memos for different pivots
4. **Export for decks**: HTML output can inform pitch deck creation

### For VCs/Analysts

1. **Batch processing**: Use auto mode for screening deal flow
2. **Supplement, don't replace**: Use as first-pass filter
3. **Check citations**: Verify critical claims before decisions
4. **Track over time**: Memory accumulates market knowledge

### For Product Teams

1. **Competitive research**: Focus prompts on specific competitor spaces
2. **Market sizing**: Use for TAM/SAM analysis
3. **Feature prioritization**: Research specific feature markets
4. **Positioning**: Understand competitive positioning options

## Running Evaluations

FounderMode includes a benchmark and evaluation system for measuring output quality.

### Prerequisites

You need a LangSmith account and API key:
```bash
export LANGCHAIN_API_KEY="ls-..."
export LANGCHAIN_TRACING_V2=true
```

### Create Benchmark Dataset

First, create the benchmark dataset in LangSmith:

```bash
# Local
uv run python scripts/create_benchmark.py

# Docker
docker compose run --rm app python scripts/create_benchmark.py
```

This creates "FounderMode Benchmark v1" with diverse test cases.

### Run Evaluations

Execute the full evaluation suite:

```bash
# Local
uv run python scripts/run_evals.py

# Docker
docker compose run --rm app python scripts/run_evals.py
```

Results are logged to LangSmith for visualization and comparison.

### Evaluation Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Investor Score** | Overall memo quality (1-10) | >7.0 |
| **Hallucination Rate** | Claims without citations | <20% |
| **Analytical Depth** | Presence of "Why now?", moats, unit economics | 4+/5 |

### Viewing Results

Access your results at [smith.langchain.com](https://smith.langchain.com):
1. Navigate to your project
2. View experiment runs and traces
3. Compare scores across experiments

## Advanced Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...          # OpenAI API access
TAVILY_API_KEY=tvly-...        # Web search API

# Optional
MODEL_NAME=gpt-4o              # LLM model (default: gpt-4o)
FM_LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR
FM_CHROMA_DB_PATH=.chroma_db   # Vector store location
```

### Model Selection

Different models offer trade-offs:

| Model | Cost | Speed | Quality |
|-------|------|-------|---------|
| `gpt-4o` | Medium | Fast | High |
| `gpt-4-turbo` | Medium | Medium | High |
| `gpt-3.5-turbo` | Low | Very Fast | Medium |

Set via:
```bash
export MODEL_NAME=gpt-4o
```

---

[← Back to Documentation Index](./README.md)
