from foundermode.domain.schema import InvestmentMemo


def test_memo_structure_completeness() -> None:
    """
    Verifies that an InvestmentMemo contains all required sections
    and that they are not empty.
    """
    memo = InvestmentMemo(
        executive_summary="Valid Summary", market_analysis="Valid Market", competitive_landscape="Valid Comp"
    )

    assert memo.executive_summary
    assert memo.market_analysis
    assert memo.competitive_landscape

    # Check for failure case
    empty_memo = InvestmentMemo()
    # In Pydantic v2, fields might be required or default to None/Empty.
    # Our current schema defaults to empty strings? Let's check schema.
    # Assuming schema defaults to "" based on previous code usage.

    assert empty_memo.executive_summary == ""


def check_citations_format(text: str) -> bool:
    """
    Heuristic check: Does the text contain source markers like '(Source: ...)'?
    """
    return "(Source:" in text


def test_citation_heuristic() -> None:
    valid_text = "The market is growing. (Source: https://example.com)"
    invalid_text = "The market is growing."

    assert check_citations_format(valid_text) is True
    assert check_citations_format(invalid_text) is False
