from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import FounderState
from foundermode.graph.nodes.researcher import EvaluatedFact, FactList, researcher_node

# Complex HTML simulating a pricing page with tables, divs, etc.
STRIPE_PRICING_MOCK = """
<html>
<body>
    <div id="pricing-table">
        <div class="plan">
            <h2>Standard</h2>
            <span class="price">2.9% + 30¢</span>
            <p>Per successful card charge</p>
        </div>
        <div class="features">
            <ul>
                <li>Global payments</li>
                <li>Fraud protection</li>
            </ul>
        </div>
    </div>
    <script>
        // Some JS that might hide things if not rendered,
        // but our scraper handles static extraction too.
    </script>
</body>
</html>
"""


@pytest.mark.e2e
@pytest.mark.slow
def test_e2e_deep_research_hard_target_simulation() -> None:
    """
    Simulates a full run of the researcher node against a 'hard' target (mocked).
    Verifies that deep scraping is triggered, content is extracted, and facts are stored.
    """
    state: FounderState = {
        "research_question": "Stripe pricing model",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "init",
        "research_topic": "Stripe pricing model",
        "search_history": [],
        "critique_history": [],
        "revision_count": 0,
    }

    # Mock Tavily to return the target URL
    mock_search = [{"url": "https://stripe.com/pricing", "title": "Stripe Pricing", "content": "Payments platform..."}]

    # Mock Selector to choose it
    mock_selection = MagicMock()
    mock_selection.urls = ["https://stripe.com/pricing"]

    # Mock Extractor to find the 2.9% fact
    mock_facts = FactList(
        facts=[
            EvaluatedFact(
                content="Standard plan is 2.9% + 30 cents",
                source_url="https://stripe.com/pricing",
                relevance_score=0.95,
            )
        ]
    )

    with patch("foundermode.graph.nodes.researcher.TavilySearch") as MockSearch:
        MockSearch.return_value.invoke.return_value = mock_search

        with patch("foundermode.graph.nodes.researcher.get_selector_chain") as MockSelector:
            MockSelector.return_value.invoke.return_value = mock_selection

            # Mock the deep_scrape_url tool to return our complex HTML (as text after processing)
            # In reality, the tool returns cleaned text. So we mock that return value.
            # But to verify it "handled" the hard target, we'd ideally mock the scraper internals.
            # Here we just check the flow.

            cleaned_text = "Standard 2.9% + 30¢ Per successful card charge Global payments Fraud protection"

            with patch("foundermode.graph.nodes.researcher.deep_scrape_url") as mock_tool:
                mock_tool.ainvoke = AsyncMock(return_value=cleaned_text)

                with patch("foundermode.graph.nodes.researcher.get_extractor_chain") as MockExtractor:
                    MockExtractor.return_value.invoke.return_value = mock_facts

                    with patch("foundermode.graph.nodes.researcher.ChromaManager") as MockMemory:
                        result = researcher_node(state)

                        # Verify we got the fact
                        facts = result["research_facts"]
                        assert len(facts) >= 1
                        assert "2.9%" in facts[0].content

                        # Verify memory storage called
                        MockMemory.return_value.add_scraped_text.assert_called_once()
                        # Verify the text passed to memory was our 'cleaned' text
                        args = MockMemory.return_value.add_scraped_text.call_args
                        assert args[0][1] == cleaned_text
