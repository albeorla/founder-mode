# Getting Started

This guide walks you through installing FounderMode, configuring your API keys, and running your first analysis.

## Prerequisites

- **[Docker](https://www.docker.com/)** - Recommended for production use
- **Python 3.12+ & [uv](https://github.com/astral-sh/uv)** - For local development
- **OpenAI API Key** - Powers the AI reasoning (GPT-4o)
- **Tavily API Key** - Enables web search capabilities

## Installation

### Option 1: Docker (Recommended)

Docker is the **"Happy Path"** that ensures all dependencies (Playwright browsers, OS libraries) are correctly configured out of the box. This avoids common issues like "Playwright not found" or shared library errors.

```bash
# Clone the repository
git clone https://github.com/your-org/founder-mode.git
cd founder-mode

# Build the container
docker compose build
```

### Option 2: Local Development

For contributors or those who prefer running natively:

```bash
# Clone the repository
git clone https://github.com/your-org/founder-mode.git
cd founder-mode

# Install Python dependencies with uv
uv sync

# Install Playwright browsers (required for deep research/scraping)
uv run playwright install chromium
```

> **Note:** The `playwright install chromium` step is critical for the Deep Research features. Without it, web scraping will fail.

## Configuration

FounderMode requires two API keys to function:

### 1. OpenAI API Key

Get your key from [OpenAI Platform](https://platform.openai.com/api-keys).

```bash
export OPENAI_API_KEY="sk-..."
```

### 2. Tavily API Key

Get your key from [Tavily](https://tavily.com/). Free tier available.

```bash
export TAVILY_API_KEY="tvly-..."
```

### Using a .env File (Recommended)

Create a `.env` file in your project directory:

```env
OPENAI_API_KEY=sk-your-openai-key
TAVILY_API_KEY=tvly-your-tavily-key
MODEL_NAME=gpt-4o
FM_LOG_LEVEL=INFO
```

FounderMode automatically loads this file on startup.

### Optional Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_NAME` | `gpt-4o` | OpenAI model to use |
| `FM_LOG_LEVEL` | `INFO` | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |
| `FM_CHROMA_DB_PATH` | `.chroma_db` | Vector database storage location |

## Your First Analysis

### Using Docker (Recommended)

```bash
# Interactive mode (default)
docker compose run --rm app run "A marketplace connecting local farmers with restaurant chefs"

# Auto mode (skip approval prompts)
docker compose run --rm app run --auto "A marketplace connecting local farmers with restaurant chefs"
```

### Using Local Installation

```bash
foundermode run "A marketplace connecting local farmers with restaurant chefs"
```

The system will:
1. **Plan** the research strategy
2. **Pause** for your approval before searching (Human-in-the-Loop)
3. **Research** the market via web search
4. **Write** an investment memo
5. **Critique** and refine the analysis
6. **Output** the final HTML report

### Auto Mode (Local)

Skip the approval step for fully autonomous operation:

```bash
foundermode run --auto "Your business idea"
# or
foundermode run -a "Your business idea"
```

## Understanding the Output

### During Execution

You'll see progress updates as the system works:

```
[Planner] Analyzing research priorities...
[Planner] Decision: Research "farm-to-table marketplace competitors"

>>> Researcher wants to search for: farm-to-table marketplace competitors
>>> Continue? [Y/n]: y

[Researcher] Searching web...
[Researcher] Found 5 relevant sources
[Researcher] Deep scraping competitor pages...

[Writer] Synthesizing investment memo...

[Critic] Reviewing analysis...
[Critic] Verdict: APPROVED - Analysis meets quality standards
```

### Final Output

The system generates an HTML report saved to your working directory:

```
memo_output.html
```

Open this file in any browser to view the formatted Investment Memo.

## Example Session

```bash
$ foundermode run "AI-powered inventory management for small retail stores"

FounderMode - Autonomous Due Diligence Agent
============================================

[Planner] Initializing research for: AI-powered inventory management for small retail stores

Research Plan:
1. Market size for retail inventory management software
2. Existing AI/ML inventory solutions
3. Pain points for small retail stores
4. Competitive pricing analysis

>>> Proceed with research? [Y/n]: y

[Researcher] Executing search: "retail inventory management software market size 2024"
[Researcher] Found 8 sources, selecting top 3 for deep analysis...
[Researcher] Extracted 12 facts from search results

[Planner] Next focus: competitor analysis
...

[Writer] Generating Investment Memo...

[Critic] Evaluating memo quality...
[Critic] APPROVED - Analysis includes:
  ✓ Market sizing with TAM/SAM
  ✓ 5 competitor profiles with pricing
  ✓ Identified risks and moats
  ✓ All claims properly cited

Output saved to: memo_output.html
```

## Troubleshooting

### "API key not found"

Ensure your environment variables are set:

```bash
echo $OPENAI_API_KEY
echo $TAVILY_API_KEY
```

Or verify your `.env` file is in the current directory.

### "Mock data" warnings

If you see mock data in outputs, the system couldn't connect to APIs. Check:
- API keys are valid and not expired
- You have network connectivity
- API rate limits haven't been exceeded

### Playwright / Browser errors (Local Development)

If you see errors like "Playwright not found" or "chromium not found":

```bash
# Install Playwright browsers
uv run playwright install chromium

# On Linux, you may also need system dependencies
uv run playwright install-deps chromium
```

> **Tip:** Using Docker avoids these issues entirely—browsers are pre-installed in the container.

### Docker-specific issues

**Build fails with network errors:**
```bash
# Retry with no cache
docker compose build --no-cache
```

**Container can't find API keys:**
Ensure your `.env` file exists and contains valid keys:
```bash
ls -la .env
cat .env | head -2  # Verify keys are present (don't share output!)
```

**Volume permission errors:**
On some systems, you may need to adjust permissions:
```bash
# Reset ownership (Linux/macOS)
sudo chown -R $(whoami) .
```

### Slow performance

Deep scraping competitor pages takes time. For faster results:
- The system caches searches in ChromaDB
- Subsequent queries on similar topics are faster
- Use `FM_LOG_LEVEL=DEBUG` to see what's happening

## Next Steps

- Read the [User Guide](./user-guide.md) for advanced options
- Explore the [Architecture](./architecture.md) to understand the system
- View [Diagrams](./diagrams/) for visual explanations

---

[← Back to Documentation Index](./README.md)
