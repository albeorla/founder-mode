from unittest.mock import MagicMock, patch

from foundermode.domain.schema import InvestmentMemo, ResearchFact
from foundermode.domain.state import FounderState
from foundermode.graph.nodes.writer import writer_node


def test_writer_fallback_when_no_api_key() -> None:
    facts = [
        ResearchFact(content="Airbnb has a strong brand.", source="S1", relevance_score=1.0),
    ]
    state: FounderState = {
        "research_question": "Airbnb",
        "research_facts": facts,
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "write",
        "research_topic": None,
        "search_history": [],
        "critique_history": [],
        "revision_count": 0,
    }

    with patch("foundermode.graph.nodes.writer.settings") as mock_settings:
        mock_settings.openai_api_key = None

        with patch("foundermode.graph.nodes.writer.get_writer_chain") as mock_get_chain:
            mock_get_chain.return_value = None

            result = writer_node(state)

            assert "memo_draft" in result
            assert "Mock" in result["memo_draft"].executive_summary
            assert "Airbnb" in result["memo_draft"].executive_summary
            assert result["next_step"] == "finish"


def test_writer_live_mode_calls_llm() -> None:
    state: FounderState = {
        "research_question": "Airbnb",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "write",
        "research_topic": None,
        "search_history": [],
        "critique_history": [],
        "revision_count": 0,
    }

    with patch("foundermode.graph.nodes.writer.settings") as mock_settings:
        mock_settings.openai_api_key = "fake-key"

        with patch("foundermode.graph.nodes.writer.get_writer_chain") as mock_get_chain:
            mock_chain = MagicMock()
            mock_get_chain.return_value = mock_chain
            mock_chain.invoke.return_value = InvestmentMemo(
                executive_summary="Real Summary",
                market_analysis="Real Market",
                competitive_landscape="Real Competition",
            )

            result = writer_node(state)

            assert result["memo_draft"].executive_summary == "Real Summary"
            assert result["next_step"] == "finish"
            mock_chain.invoke.assert_called_once()
