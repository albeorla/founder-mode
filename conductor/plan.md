# Project Plan: FounderMode

## Track 1: The Skeleton & State
**Goal:** A running CLI that executes a dummy LangGraph workflow. Validation of the new stack.
- [x] Task: Initialize project structure.
    - Set up `pyproject.toml` with dependencies (langgraph, chroma, fastapi).
    - Configure `ruff`, `mypy`, and `pytest`.
    - Create directory tree: `src/foundermode/{domain,graph,memory,tools,api}`.
- [ ] Task: Define Domain Models (`domain/schema.py`).
    - Define `ResearchPlan`, `ResearchFact`, and `InvestmentMemo` Pydantic models.
- [ ] Task: Define Graph State (`domain/state.py`).
    - Define `GraphState` TypedDict (input query, gathered facts, draft sections).
- [ ] Task: Implement a Mock Analyst Node (`graph/nodes/mock.py`).
    - Create a simple node that accepts state and returns hardcoded "analysis" to prove the graph works.
- [ ] Task: Wire the Skeleton Graph (`graph/workflow.py`).
    - Connect `START` -> `MockAnalyst` -> `END`.
    - Setup **LangSmith** tracing (env vars).
- [ ] Task: Build the CLI Entry Point (`api/cli.py`).
    - Implement `foundermode run "My Idea"` command.
- [ ] Task: Checkpoint - Verify Skeleton.
    - Run the CLI and confirm it prints the mock output.

## Track 2: The Research Tools
**Goal:** Give the agent "Hands" to interact with the world.
- [ ] Task: Implement Tavily Search Tool (`tools/search.py`).
    - Wrap Tavily API into a LangChain `BaseTool`.
    - Ensure it returns structured results (URL, Snippet, Content).
- [ ] Task: Implement Web Scraper (`tools/scrape.py`).
    - Build a `BeautifulSoup` scraper to extract text from specific URLs found by search.
- [ ] Task: Create `ResearchTask` Domain Logic.
    - Define logic for "What needs to be researched?" vs "What has been found?".

## Track 3: The Vector Brain (Memory)
**Goal:** Give the agent "Long-term Working Memory" (RAG).
- [ ] Task: Implement Chroma Manager (`memory/vector_store.py`).
    - Create `ChromaManager` class.
    - Implement `add_facts(facts)` using OpenAI Embeddings.
    - Implement `query_similar(query)` to find relevant context.
- [ ] Task: Update Tools to Auto-Archive.
    - Modify `tools/search.py` to automatically save successful search results into Chroma.
- [ ] Task: Checkpoint - Verify Memory.
    - Run a script that searches for "Competitors to AirBnB", saves results, and then queries "Who are AirBnB rivals?" to prove retrieval works.

## Track 4: The Logic Loops (The Brain)
**Goal:** Replace the Mock Analyst with real AI Agents.
- [ ] Task: Implement the Analyst Node (`graph/nodes/analyst.py`).
    - Prompt Engineering: "You are a VC Analyst. Given the user idea, what do you need to know?"
    - Output: A list of `ResearchTasks`.
- [ ] Task: Implement the Researcher Node (`graph/nodes/researcher.py`).
    - Logic: Take `ResearchTask`, execute `TavilySearch`, store results.
- [ ] Task: Define Conditional Edges (`graph/edges.py`).
    - Implement `should_continue`: If `state.missing_info` is not empty -> Go to Researcher. Else -> Go to Writer.
- [ ] Task: Implement the Writer Node (`graph/nodes/writer.py`).
    - Logic: Query Vector Store for relevant facts -> Generate Investment Memo Markdown.

## Track 5: Interface & Polish
**Goal:** Production-ready output and Human-in-the-loop.
- [ ] Task: Implement Report Generator.
    - Convert Markdown output to a clean PDF or HTML format.
- [ ] Task: Add Human-in-the-loop Breakpoint.
    - Pause graph after "Analyst Plan" to let user approve/edit the research direction.
- [ ] Task: Expose via FastAPI (`api/server.py`).
    - Create endpoints for `POST /run` and `GET /status/{run_id}`.
