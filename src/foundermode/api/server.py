import uuid
from typing import Any

from fastapi import FastAPI, HTTPException
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel

from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import GraphState
from foundermode.graph.workflow import create_workflow

app = FastAPI(title="FounderMode API", version="0.1.0")


# For the prototype, we use an in-memory checkpointer.

# In production, this would be a persistent store (SQLite, Postgres).

memory = MemorySaver()

workflow = create_workflow(checkpointer=memory)


class RunRequest(BaseModel):
    idea: str


class RunResponse(BaseModel):
    run_id: str

    status: str


class StatusResponse(BaseModel):
    run_id: str

    next_node: str | None

    state: dict[str, Any]


@app.get("/")  # type: ignore[misc]
async def read_root() -> dict[str, str]:
    return {"message": "FounderMode API is running"}


@app.get("/health")  # type: ignore[misc]
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/run", response_model=RunResponse)  # type: ignore[misc]
async def create_run(request: RunRequest) -> RunResponse:
    run_id = str(uuid.uuid4())

    config: RunnableConfig = {"configurable": {"thread_id": run_id}}

    # Initialize state

    initial_state: GraphState = {
        "research_question": request.idea,
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "init",
        "research_topic": None,
    }

    # Start the graph in the background (or just synchronously for this simple API)

    # LangGraph's .invoke with a checkpointer will run until the first interrupt.

    try:
        workflow.invoke(initial_state, config=config)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return RunResponse(run_id=run_id, status="started")


@app.get("/run/{run_id}", response_model=StatusResponse)  # type: ignore[misc]
async def get_run_status(run_id: str) -> StatusResponse:
    config: RunnableConfig = {"configurable": {"thread_id": run_id}}

    snapshot = workflow.get_state(config)

    if not snapshot.values:
        raise HTTPException(status_code=404, detail="Run not found")

    next_node = snapshot.next[0] if snapshot.next else None

    return StatusResponse(run_id=run_id, next_node=next_node, state=snapshot.values)
