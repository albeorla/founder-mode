from operator import add
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage

from foundermode.domain.schema import InvestmentMemo, ResearchFact, ResearchPlan


class GraphState(TypedDict):
    """The state of the FounderMode research graph."""

    query: str
    plan: ResearchPlan
    facts: Annotated[list[ResearchFact], add]
    draft: InvestmentMemo
    messages: Annotated[list[BaseMessage], add]
