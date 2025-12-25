from unittest.mock import AsyncMock, MagicMock, patch

from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import FounderState
from foundermode.graph.nodes.researcher import researcher_node


def test_researcher_node_deep_scrape_flow() -> None:
    # 1. Setup initial state
    state: FounderState = {
        "research_question": "Airbnb pricing model",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "init",
        "research_topic": "Airbnb pricing model",
        "critique_history": [],
        "revision_count": 0,
    }

    # 2. Mock Tavily Search to return some URLs
    mock_search_results = [
        {"url": "https://airbnb.com/pricing", "title": "Airbnb Pricing", "content": "Official pricing info"},
        {"url": "https://news.com/airbnb", "title": "News", "content": "News snippet"},
    ]

    # 3. Mock URL Selector to choose the pricing URL
    mock_selection = MagicMock()
    mock_selection.urls = ["https://airbnb.com/pricing"]

    # 4. Mock Scraper to return full page text
    mock_scraped_text = "This is the full text of Airbnb pricing page. " + "Detailed info " * 100

    # 5. Mock Extractor to return facts from the full text
    mock_extracted_facts = MagicMock()
    mock_extracted_facts.facts = [
        MagicMock(content="Airbnb take rate is 14%", source_url="https://airbnb.com/pricing", relevance_score=0.9)
    ]

    # Patch everything
    with patch("foundermode.graph.nodes.researcher.TavilySearch") as MockSearch:
        MockSearch.return_value.invoke.return_value = mock_search_results

        with patch("foundermode.graph.nodes.researcher.get_selector_chain") as MockSelector:
            MockSelector.return_value.invoke.return_value = mock_selection

            with patch("foundermode.graph.nodes.researcher.deep_scrape_url") as mock_tool:
                mock_tool.ainvoke = AsyncMock(return_value=mock_scraped_text)
                with patch("foundermode.graph.nodes.researcher.get_extractor_chain") as MockExtractor:
                    MockExtractor.return_value.invoke.return_value = mock_extracted_facts

                    with patch("foundermode.graph.nodes.researcher.ChromaManager") as MockMemory:
                        # Invoke node
                        result = researcher_node(state)

                        # Verify results
                        assert "research_facts" in result
                        # Check that we have facts from the deep scrape
                        facts = result["research_facts"]
                        assert len(facts) > 0
                        # Check that memory was updated with scraped text
                        MockMemory.return_value.add_scraped_text.assert_called_once()
                        # Check transition
                        assert result["next_step"] == "planner"
