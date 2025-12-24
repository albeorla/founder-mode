from unittest.mock import patch

from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import FounderState
from foundermode.graph.nodes.planner import planner_node


def test_planner_decides_research() -> None:
    state: FounderState = {
        "research_question": "Airbnb business model",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "init",
        "research_topic": None,
    }

    # We need to mock the LLM call inside the node.
    # Since we haven't implemented the node, we will assume it uses a structured output or tool calling.

    with patch("foundermode.graph.nodes.planner.ChatOpenAI") as _:
        # Mock the invoke return value
        # mock_llm_instance = MockLLM.return_value
        # Assuming the planner returns a structured object that dictates the next step
        # For now, let's assume simple logic: if no facts, research.

        # Actually, for the TDD, I'll write the test assuming the node exists and logic is implemented.
        # But I need to control the LLM decision.

        # Let's mock the chain invokation
        with patch("foundermode.graph.nodes.planner.planner_chain") as mock_chain:
            mock_chain.invoke.return_value = {"action": "research", "reason": "Need more info"}

            result = planner_node(state)

            assert result["next_step"] == "research"


def test_planner_decides_write() -> None:
    state: FounderState = {
        "research_question": "Airbnb business model",
        "research_facts": [],  # Assume facts exist, but for mocking it doesn't matter
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "init",
        "research_topic": None,
    }

    with patch("foundermode.graph.nodes.planner.planner_chain") as mock_chain:
        mock_chain.invoke.return_value = {"action": "write", "reason": "Sufficient info"}

        result = planner_node(state)

        assert result["next_step"] == "write"
