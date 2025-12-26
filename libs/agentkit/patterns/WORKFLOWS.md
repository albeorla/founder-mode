# LangGraph Workflow Patterns with AgentKit

This document provides copy-pasteable patterns for common agentic workflows using LangGraph and AgentKit.

## 1. Linear Chain (Research -> Write)

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from agentkit import create_llm, ExtractionService

class State(TypedDict):
    url: str
    content: str
    summary: str

async def research_node(state: State):
    extractor = ExtractionService()
    content = await extractor.extract(state["url"])
    return {"content": content}

async def write_node(state: State):
    llm = create_llm()
    resp = await llm.ainvoke(f"Summarize this: {state['content']}")
    return {"summary": resp.content}

workflow = StateGraph(State)
workflow.add_node("research", research_node)
workflow.add_node("write", write_node)
workflow.set_entry_point("research")
workflow.add_edge("research", "write")
workflow.add_edge("write", END)
app = workflow.compile()
```

## 2. Research Loop (Search -> Extract -> Evaluate -> Repeat)

```python
class ResearchState(TypedDict):
    query: str
    facts: list[str]
    is_sufficient: bool

# ... nodes for search, extract, evaluate ...

workflow = StateGraph(ResearchState)
workflow.add_node("search", search_node)
workflow.add_node("evaluate", evaluate_node)

workflow.add_conditional_edges(
    "evaluate",
    lambda x: "complete" if x["is_sufficient"] else "search",
    {"complete": END, "search": "search"}
)
```

## 3. Council Pattern (Multi-Model Consensus)

Collect opinions from multiple models and synthesize a final answer.

```python
async def council_node(state: State):
    models = ["gpt-4o", "claude-3-opus-20240229"]
    tasks = [create_llm(m).ainvoke(state["prompt"]) for m in models]
    results = await asyncio.gather(*tasks)

    # Synthesis
    synthesis_llm = create_llm("gpt-4o")
    final = await synthesis_llm.ainvoke(f"Synthesize these answers: {results}")
    return {"answer": final.content}
```
