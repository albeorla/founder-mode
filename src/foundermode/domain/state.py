import operator
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage

from foundermode.domain.schema import InvestmentMemo, ResearchFact


class FounderState(TypedDict):
    """The persistent state of the FounderMode agent."""

    research_question: str
    """The original question or idea from the user."""

    research_facts: Annotated[list[ResearchFact], operator.add]
    """Accumulated list of research facts. Merged by addition."""

    memo_draft: InvestmentMemo
    """The current draft of the investment memo."""

    research_topic: str | None
    """The specific topic currently being researched."""

    messages: Annotated[list[BaseMessage], operator.add]
    """Chat history for the planner/agent conversation."""

    next_step: str
    """The next node to execute (e.g., 'research', 'write', 'finish')."""


# Backward compatibility alias
GraphState = FounderState
