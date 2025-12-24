from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FounderMode API", version="0.1.0")


class RunRequest(BaseModel):
    idea: str


class RunResponse(BaseModel):
    run_id: str
    status: str


@app.get("/")  # type: ignore[misc]
async def read_root() -> dict[str, str]:
    return {"message": "FounderMode API is running"}


@app.get("/health")  # type: ignore[misc]
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
