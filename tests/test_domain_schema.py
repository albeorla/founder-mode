import pytest
from pydantic import ValidationError
from foundermode.domain.schema import ResearchPlan, ResearchFact, InvestmentMemo

def test_research_fact_valid() -> None:
    fact = ResearchFact(source="https://example.com", content="Test fact content")
    assert fact.source == "https://example.com"
    assert fact.content == "Test fact content"

def test_research_plan_valid() -> None:
    plan = ResearchPlan(tasks=["Task 1", "Task 2"])
    assert plan.tasks == ["Task 1", "Task 2"]

def test_investment_memo_valid() -> None:
    memo = InvestmentMemo(
        executive_summary="Summary",
        market_analysis="Analysis",
        competitive_landscape="Landscape"
    )
    assert memo.executive_summary == "Summary"
