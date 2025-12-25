from pathlib import Path

from foundermode.domain.schema import InvestmentMemo
from foundermode.tools.reporter import render_memo


def test_render_memo_output(tmp_path: Path) -> None:
    """Test that render_memo produces an HTML file with the correct content."""
    # 1. Setup Data
    memo = InvestmentMemo(
        executive_summary="Summary content",
        market_analysis="Market content",
        competitive_landscape="Competitors content",
    )

    filename = tmp_path / "test_memo.html"

    # 2. Invoke
    html_content = render_memo(memo, str(filename))

    # 3. Assert
    assert '<html lang="en">' in html_content
    assert "Summary content" in html_content
    assert "Market content" in html_content
    assert "Competitors content" in html_content

    # Verify file was written
    assert filename.exists()
    assert "Summary content" in filename.read_text()
