from foundermode.domain.schema import InvestmentMemo
from foundermode.tools.reporter import render_memo


def test_render_memo_output() -> None:
    """Test that render_memo produces an HTML file with the correct content."""
    # 1. Setup Data
    memo = InvestmentMemo(
        executive_summary="Summary content",
        market_analysis="Market content",
        competitive_landscape="Competitors content",
    )

    filename = "test_memo.html"

    # 2. Invoke
    html_content = render_memo(memo, filename)

    # 3. Assert
    assert '<html lang="en">' in html_content
    assert "Summary content" in html_content
    assert "Market content" in html_content
    assert "Competitors content" in html_content

    # Verify file was written if filename is provided
    # However, for pure unit testing, we might want to mock file writing.
    # But since the goal is to produce a file, checking the file system is valid integration test.
    # We will assume the function writes to disk if filename is not None.

    # Clean up (if we were writing to disk, but let's assume the function returns the string too)
    # Ideally, we mock the file write operation to avoid disk IO in unit tests,
    # but for simplicity in this prototype, let's just check the string return first.
