from unittest.mock import MagicMock, patch

from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import FounderState
from foundermode.graph.workflow import create_workflow


def test_e2e_graceful_fallback() -> None:
    """
    Verifies that the graph can run from start to finish using mock fallbacks
    when no API keys are present.
    """
    # 1. Force mock mode by clearing keys in settings
    with patch("foundermode.config.settings") as mock_settings:
        mock_settings.openai_api_key = None
        mock_settings.tavily_api_key = None
        mock_settings.model_name = "gpt-4o"
        mock_settings.chroma_db_path = ".chroma_db_test"

        # 2. Create the real workflow (it will use the mocked settings)
        # We must also mock the internal imports in nodes if they use the global 'settings' instance
        # instead of the one we just patched.
        # Actually, if they do 'from foundermode.config import settings', they get the instance.
        # Patching 'foundermode.config.settings' should affect all modules importing it.

        with (
            patch("foundermode.graph.nodes.planner.settings", mock_settings),
            patch("foundermode.graph.nodes.writer.settings", mock_settings),
            patch("foundermode.tools.search.settings", mock_settings),
            patch("foundermode.memory.vector_store.settings", mock_settings),
        ):
            app = create_workflow(interrupt_before=[])

            initial_state: FounderState = {
                "research_question": "A new AI-powered coffee machine",
                "research_facts": [],
                "memo_draft": InvestmentMemo(),
                "messages": [],
                "next_step": "init",
                "research_topic": None,
            }

            # Execute the full graph
            # It should loop researcher 3 times (based on our mock logic in planner) then write.
            final_state = app.invoke(initial_state)

            # 3. Verify Final State
            assert final_state["memo_draft"].executive_summary != ""
            assert "Mock" in final_state["memo_draft"].executive_summary
            assert len(final_state["research_facts"]) >= 3
            assert final_state["next_step"] == "finish"


def test_e2e_live_smoke() -> None:
    """
    Verifies the code path for live mode when API keys are present,
    but mocks the actual LLM and search calls.
    """
    with patch("foundermode.config.settings") as mock_settings:
        mock_settings.openai_api_key = "sk-fake"
        mock_settings.tavily_api_key = "tvly-fake"
        mock_settings.model_name = "gpt-4o"
        mock_settings.chroma_db_path = ".chroma_db_test_live"

        with (
            patch("foundermode.graph.nodes.planner.get_planner_chain") as mock_get_planner,
            patch("foundermode.graph.nodes.writer.get_writer_chain") as mock_get_writer,
            patch("foundermode.tools.search.TavilySearch._run") as mock_search_run,
        ):
            # Mock Planner to research then write
            mock_planner_chain = MagicMock()
            mock_get_planner.return_value = mock_planner_chain
            mock_planner_chain.invoke.side_effect = [
                {"action": "research", "research_topic": "AI Trends", "reason": "More info"},
                {"action": "write", "research_topic": None, "reason": "Enough"},
            ]

            # Mock Writer
            mock_writer_chain = MagicMock()
            mock_get_writer.return_value = mock_writer_chain
            mock_writer_chain.invoke.return_value = InvestmentMemo(executive_summary="Real-ish Memo")

            # Mock Search Tool
            mock_search_run.return_value = [{"content": "Live-ish fact", "url": "http://live", "score": 0.99}]

            # Mock Chroma to avoid real embeddings
            with patch("foundermode.memory.vector_store.ChromaManager") as mock_chroma:
                mock_chroma_instance = mock_chroma.return_value
                mock_chroma_instance.query_similar.return_value = []

                app = create_workflow(interrupt_before=[])

                initial_state: FounderState = {
                    "research_question": "A new AI-powered coffee machine",
                    "research_facts": [],
                    "memo_draft": InvestmentMemo(),
                    "messages": [],
                    "next_step": "init",
                    "research_topic": None,
                }

                final_state = app.invoke(initial_state)

                assert final_state["memo_draft"].executive_summary == "Real-ish Memo"
                assert mock_planner_chain.invoke.call_count == 2
                assert mock_search_run.called
