from unittest.mock import patch

from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import FounderState
from foundermode.graph.nodes.researcher import EvaluatedFact, FactList, researcher_node


def test_researcher_fallback_when_search_fails() -> None:
    state: FounderState = {
        "research_question": "Airbnb",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "research",
        "research_topic": "Airbnb business model",
        "search_history": [],
        "critique_history": [],
        "revision_count": 0,
    }

    # Mock TavilySearch to raise error (e.g. missing API key)
    with patch("foundermode.graph.nodes.researcher.TavilySearch") as MockTool:
        mock_tool_instance = MockTool.return_value
        mock_tool_instance.invoke.side_effect = ValueError("TAVILY_API_KEY must be set")

        # Mock ChromaManager
        with patch("foundermode.graph.nodes.researcher.ChromaManager") as _:
            # Run node
            result = researcher_node(state)

            # Verify it uses fallback logic
            assert "research_facts" in result
            assert len(result["research_facts"]) == 1
            assert "Mock Fact" in result["research_facts"][0].content
            assert result["next_step"] == "planner"


def test_researcher_success() -> None:
    state: FounderState = {
        "research_question": "Airbnb",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "research",
        "research_topic": "Airbnb business model",
        "search_history": [],
        "critique_history": [],
        "revision_count": 0,
    }

    with patch("foundermode.graph.nodes.researcher.TavilySearch") as MockTool:
        mock_tool_instance = MockTool.return_value
        mock_tool_instance.invoke.return_value = [{"content": "Live result", "url": "http", "score": 0.9}]

        with patch("foundermode.graph.nodes.researcher.ChromaManager") as _:
            # Mock the selector chain to avoid deep scraping
            with patch("foundermode.graph.nodes.researcher.get_selector_chain") as mock_get_selector:
                mock_get_selector.return_value = None

                # Mock the extractor chain
                with patch("foundermode.graph.nodes.researcher.get_extractor_chain") as mock_get_chain:
                    mock_chain = mock_get_chain.return_value
                    # Make it return a valid FactList
                    mock_chain.invoke.return_value = FactList(
                        facts=[EvaluatedFact(content="Extracted Fact", source_url="http", relevance_score=0.9)]
                    )

                    result = researcher_node(state)

                    assert len(result["research_facts"]) == 1
                    assert "Extracted Fact" in result["research_facts"][0].content
