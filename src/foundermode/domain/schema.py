from pydantic import BaseModel, Field


class ResearchFact(BaseModel):
    """A single verified piece of information."""

    source: str = Field(description="The URL or source of the information")
    content: str = Field(description="The actual content or snippet of information")


class ResearchPlan(BaseModel):
    """A list of questions/tasks to be researched."""

    tasks: list[str] = Field(default_factory=list, description="List of research questions or tasks")


class InvestmentMemo(BaseModel):
    """The final output structure for the investment analysis."""

    executive_summary: str = Field(default="", description="High-level summary of the idea")
    market_analysis: str = Field(default="", description="Analysis of the market opportunity")
    competitive_landscape: str = Field(default="", description="Analysis of competitors and their positioning")
