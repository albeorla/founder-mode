from unittest.mock import patch

from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import FounderState
from foundermode.graph.nodes.researcher import researcher_node


def test_researcher_performs_search_and_stores_facts() -> None:
    state: FounderState = {
        "research_question": "Airbnb",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "research",
        "research_topic": "Airbnb business model",
    }

    # Mock TavilySearch
    with patch("foundermode.graph.nodes.researcher.TavilySearch") as MockTool:
        mock_tool_instance = MockTool.return_value
        mock_tool_instance.invoke.return_value = "Airbnb makes money by charging service fees."

        # Mock ChromaManager
        with patch("foundermode.graph.nodes.researcher.ChromaManager") as MockChroma:
            mock_chroma_instance = MockChroma.return_value
            mock_chroma_instance.add_facts.return_value = True

            # Run node
            result = researcher_node(state)

            # Verify result has new facts
            # The node should return an update to 'research_facts'
            assert "research_facts" in result
            assert len(result["research_facts"]) == 1
            assert "service fees" in result["research_facts"][0].content

            # Verify memory interaction
            mock_chroma_instance.add_facts.assert_called()

            # Verify tool interaction
            mock_tool_instance.invoke.assert_called_with("Airbnb business model")


def test_researcher_handles_no_topic() -> None:
    # If no topic is set, it might default to research question or skip
    state: FounderState = {
        "research_question": "Airbnb",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "research",
        "research_topic": None,
    }

    with patch("foundermode.graph.nodes.researcher.TavilySearch") as MockTool:
        result = researcher_node(state)
        # Should default to question
        MockTool.return_value.invoke.assert_called_with("Airbnb")
        assert "research_facts" in result
