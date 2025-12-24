from foundermode.domain.schema import InvestmentMemo, ResearchFact, ResearchPlan, ResearchTask


def test_research_fact_valid() -> None:
    fact = ResearchFact(source="https://example.com", content="Test fact content", title="Example")
    assert fact.source == "https://example.com"
    assert fact.content == "Test fact content"
    assert fact.title == "Example"


def test_research_task_valid() -> None:
    task = ResearchTask(question="Who is the CEO?")
    assert task.question == "Who is the CEO?"
    assert task.status == "pending"
    assert len(task.results) == 0


def test_research_plan_valid() -> None:
    task = ResearchTask(question="Test question")
    plan = ResearchPlan(tasks=[task])
    assert len(plan.tasks) == 1
    assert plan.tasks[0].question == "Test question"


def test_investment_memo_valid() -> None:
    memo = InvestmentMemo(executive_summary="Summary", market_analysis="Analysis", competitive_landscape="Landscape")
    assert memo.executive_summary == "Summary"
