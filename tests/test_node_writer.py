from unittest.mock import patch

from foundermode.domain.schema import InvestmentMemo, ResearchFact
from foundermode.domain.state import FounderState
from foundermode.graph.nodes.writer import writer_node


def test_writer_generates_memo() -> None:
    facts = [
        ResearchFact(content="Airbnb has a strong brand.", source="S1", relevance_score=1.0),
        ResearchFact(content="Market size is $100B.", source="S2", relevance_score=1.0),
    ]
    state: FounderState = {
        "research_question": "Airbnb",
        "research_facts": facts,
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "write",
        "research_topic": None,
    }

    # Mock LLM chain
    with patch("foundermode.graph.nodes.writer.writer_chain") as mock_chain:
        mock_chain.invoke.return_value = InvestmentMemo(
            executive_summary="Summary", market_analysis="Market", competitive_landscape="Competition"
        )

        result = writer_node(state)

        # Verify result updates memo_draft
        assert "memo_draft" in result
        assert isinstance(result["memo_draft"], InvestmentMemo)
        assert result["memo_draft"].executive_summary == "Summary"
        assert result["next_step"] == "finish"
