from unittest.mock import MagicMock, patch

from foundermode.domain.schema import CriticVerdict, InvestmentMemo, ResearchFact
from foundermode.domain.state import FounderState
from foundermode.graph.nodes.critic import critic_node


def test_critic_node_mock_rejection() -> None:
    # Setup state with a 'Mock' memo
    state: FounderState = {
        "research_question": "Test",
        "research_facts": [],
        "memo_draft": InvestmentMemo(executive_summary="Mock Summary"),
        "messages": [],
        "next_step": "write",
        "critique_history": [],
        "revision_count": 0,
        "research_topic": None,
        "search_history": [],
    }

    # Execute node (no API key patched, uses mock logic)
    with patch("foundermode.graph.nodes.critic.get_critic_chain", return_value=None):
        result = critic_node(state)

    assert result["next_step"] == "reject"
    assert result["revision_count"] == 1
    assert "Mock Critique" in result["critique_history"][0]


def test_critic_node_mock_approval() -> None:
    # Setup state with a 'Real' memo (no "Mock" string)
    state: FounderState = {
        "research_question": "Test",
        "research_facts": [],
        "memo_draft": InvestmentMemo(executive_summary="Professional analysis of the market."),
        "messages": [],
        "next_step": "write",
        "critique_history": [],
        "revision_count": 0,
        "research_topic": None,
        "search_history": [],
    }

    with patch("foundermode.graph.nodes.critic.get_critic_chain", return_value=None):
        result = critic_node(state)

    assert result["next_step"] == "approve"
    assert result["revision_count"] == 0


def test_critic_node_live_rejection() -> None:
    # Setup state
    state: FounderState = {
        "research_question": "Test",
        "research_facts": [ResearchFact(content="High signal fact", source="S")],
        "memo_draft": InvestmentMemo(executive_summary="Weak Summary"),
        "messages": [],
        "next_step": "write",
        "critique_history": [],
        "revision_count": 0,
        "research_topic": None,
        "search_history": [],
    }

    # Mock the LLM chain to return a REJECT verdict
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = CriticVerdict(
        action="reject", feedback="Missing quantitative metrics.", missing_data=["CAC", "LTV"]
    )

    with patch("foundermode.graph.nodes.critic.get_critic_chain", return_value=mock_chain):
        result = critic_node(state)

    assert result["next_step"] == "reject"
    assert result["revision_count"] == 1
    assert "Missing quantitative metrics" in result["critique_history"][0]
