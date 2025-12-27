"""Pydantic schemas for DD-Arbiter domain models."""

from typing import Annotated
import operator

from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class ModelResponse(BaseModel):
    """Response from a single model in a specific role."""

    model: str = Field(description="Model identifier (e.g., 'gpt-4o')")
    role: str = Field(description="Role the model played ('bull', 'bear', 'analyst')")
    response: str = Field(description="Full response text")


class Claim(BaseModel):
    """A specific factual claim extracted from model responses."""

    text: str = Field(description="The specific factual claim")
    confidence: float = Field(ge=0, le=1, description="Confidence score 0-1")
    supporting_models: list[str] = Field(
        default_factory=list, description="Models that agree with this claim"
    )
    contradicting_models: list[str] = Field(
        default_factory=list, description="Models that disagree with this claim"
    )


class Disagreement(BaseModel):
    """A detected disagreement between two model claims."""

    claim_1: dict = Field(description="First claim with model and role attribution")
    claim_2: dict = Field(description="Second claim with model and role attribution")
    disagreement_type: str = Field(description="Type of disagreement (contradiction, etc.)")
    severity: str = Field(description="Severity level: high, medium, low")


class UncertaintyResult(BaseModel):
    """Result of uncertainty quantification for a response."""

    answer: str = Field(description="The consensus answer")
    confidence: float = Field(ge=0, le=1, description="Final confidence score 0-1")
    semantic_entropy: float = Field(description="Semantic entropy across samples")
    consistency_score: float = Field(description="Consistency of responses")
    num_semantic_clusters: int = Field(description="Number of distinct answer clusters")
    verbalized_confidence_avg: float = Field(description="Average verbalized confidence")


class DiligenceReport(BaseModel):
    """Structured output for CIM analysis."""

    # Summary
    thesis_confidence_score: float = Field(
        ge=0,
        le=100,
        description="Overall confidence in the investment thesis (0-100)",
    )
    executive_summary: str = Field(description="2-3 sentence summary of findings")

    # Consensus findings
    consensus_claims: list[Claim] = Field(
        default_factory=list, description="Claims all models agree on"
    )

    # Disputed findings (the value-add)
    disputed_claims: list[Claim] = Field(
        default_factory=list, description="Claims where models disagree"
    )

    # Risk assessment
    key_risks: list[str] = Field(default_factory=list, description="Top risks identified")
    deal_breakers: list[str] = Field(
        default_factory=list, description="Potential deal-killing issues"
    )

    # Action items
    diligence_questions: list[str] = Field(
        default_factory=list,
        description="Suggested questions for management/advisors",
    )

    # Meta
    needs_human_review: bool = Field(
        description="True if high uncertainty or major disagreements"
    )
    review_reason: str | None = Field(
        default=None, description="Why human review is recommended"
    )


class ResearchState(TypedDict):
    """State object for the LangGraph research workflow."""

    query: str
    document_content: str
    model_responses: Annotated[list[dict], operator.add]
    clusters: list[dict]
    disagreements: list[dict]
    uncertainty: dict
    final_answer: dict
