from unittest.mock import MagicMock, patch

from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import FounderState
from foundermode.graph.nodes.planner import planner_node


def test_planner_fallback_when_no_api_key() -> None:
    state: FounderState = {
        "research_question": "Airbnb business model",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "init",
        "research_topic": None,
        "search_history": [],
        "critique_history": [],
        "revision_count": 0,
    }

    # Mock settings to have no API key
    with patch("foundermode.graph.nodes.planner.settings") as mock_settings:
        mock_settings.openai_api_key = None

        # Ensure it doesn't try to call the real LLM by checking get_planner_chain
        with patch("foundermode.graph.nodes.planner.get_planner_chain") as mock_get_chain:
            mock_get_chain.return_value = None

            result = planner_node(state)

            # Verify it uses fallback logic
            assert result["next_step"] == "research"  # 0 facts < 3
            assert "Market size" in result["research_topic"]
            mock_get_chain.assert_called()


def test_planner_live_mode_calls_llm() -> None:
    state: FounderState = {
        "research_question": "Airbnb business model",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "init",
        "research_topic": None,
        "search_history": [],
        "critique_history": [],
        "revision_count": 0,
    }

    with patch("foundermode.graph.nodes.planner.settings") as mock_settings:
        mock_settings.openai_api_key = "fake-key"

        with patch("foundermode.graph.nodes.planner.get_planner_chain") as mock_get_chain:
            mock_chain = MagicMock()
            mock_get_chain.return_value = mock_chain
            mock_chain.invoke.return_value = {"action": "research", "research_topic": "Test Topic", "reason": "Test"}

            result = planner_node(state)

            assert result["next_step"] == "research"
            assert result["research_topic"] == "Test Topic"
            mock_chain.invoke.assert_called_once()
