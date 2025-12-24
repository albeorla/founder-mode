from pydantic import BaseModel, Field


class ResearchFact(BaseModel):
    """A single verified piece of information."""

    source: str = Field(description="The URL or source of the information")
    content: str = Field(description="The actual content or snippet of information")
    title: str | None = Field(None, description="The title of the source page")
    relevance_score: float | None = Field(None, description="How relevant this fact is to the query")


class ResearchTask(BaseModel):
    """An individual research unit of work."""

    question: str = Field(description="The specific question to be answered")
    status: str = Field(
        default="pending",
        description="The status of the task (pending, in_progress, completed, failed)",
    )
    results: list[ResearchFact] = Field(default_factory=list, description="The facts gathered for this task")


class ResearchPlan(BaseModel):
    """A list of questions/tasks to be researched."""

    tasks: list[ResearchTask] = Field(default_factory=list, description="List of research tasks")


class InvestmentMemo(BaseModel):
    """The final output structure for the investment analysis."""

    executive_summary: str = Field(default="", description="High-level summary of the idea")
    market_analysis: str = Field(default="", description="Analysis of the market opportunity")
    competitive_landscape: str = Field(default="", description="Analysis of competitors and their positioning")
