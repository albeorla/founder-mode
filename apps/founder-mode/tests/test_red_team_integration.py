from unittest.mock import MagicMock, patch

import pytest

from foundermode.domain.schema import CriticVerdict, InvestmentMemo
from foundermode.domain.state import FounderState
from foundermode.graph.workflow import create_workflow


@pytest.mark.integration
@pytest.mark.slow
def test_red_team_loop_termination() -> None:
    """
    Verifies that the graph terminates after exactly 3 rejections
    from the critic node.
    """
    # 1. Setup mocks
    # We mock the planner to always want to research, but then write
    # We mock the critic to always REJECT

    with patch("foundermode.graph.nodes.planner.get_planner_chain") as mock_planner_chain_getter:
        mock_planner = MagicMock()
        mock_planner_chain_getter.return_value = mock_planner

        # Planner behavior: research once, then write (repeatedly)
        mock_planner.invoke.side_effect = [
            {"action": "research", "research_topic": "Topic", "reason": "Reason"},
            {"action": "write", "research_topic": None, "reason": "Enough info"},  # Round 1
            {"action": "write", "research_topic": None, "reason": "Enough info"},  # Round 2
            {"action": "write", "research_topic": None, "reason": "Enough info"},  # Round 3
            {"action": "write", "research_topic": None, "reason": "Enough info"},  # Fail safe
        ]

        with patch("foundermode.graph.nodes.critic.get_critic_chain") as mock_critic_chain_getter:
            mock_critic = MagicMock()
            mock_critic_chain_getter.return_value = mock_critic

            # Critic always rejects
            mock_critic.invoke.return_value = CriticVerdict(
                action="reject", feedback="Still too fluffy.", missing_data=["Everything"]
            )

            # Mock search tool to return something
            with patch("foundermode.tools.search.TavilySearch.invoke", return_value=[]):
                # Mock writer to return a memo
                with patch("foundermode.graph.nodes.writer.get_writer_chain") as mock_writer_chain_getter:
                    mock_writer = MagicMock()
                    mock_writer_chain_getter.return_value = mock_writer
                    mock_writer.invoke.return_value = InvestmentMemo(executive_summary="Mock")

                    # Create workflow without HITL interrupts for automation
                    app = create_workflow(interrupt_before=[])

                    initial_state: FounderState = {
                        "research_question": "Idea",
                        "research_facts": [],
                        "memo_draft": InvestmentMemo(),
                        "messages": [],
                        "next_step": "init",
                        "research_topic": None,
                        "search_history": [],
                        "critique_history": [],
                        "revision_count": 0,
                    }

                    # 2. Execute
                    final_state = app.invoke(initial_state)

                    # 3. Verify
                    # It should have run:
                    # planner -> researcher -> planner -> writer -> critic (R1)
                    # -> planner -> writer -> critic (R2)
                    # -> planner -> writer -> critic (R3)
                    # -> END

                    assert final_state["revision_count"] == 3
                    assert len(final_state["critique_history"]) == 3
                    assert final_state["next_step"] == "reject"
