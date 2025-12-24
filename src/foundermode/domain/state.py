from typing import List, TypedDict, Annotated
from operator import add
from langchain_core.messages import BaseMessage
from foundermode.domain.schema import ResearchPlan, ResearchFact, InvestmentMemo

class GraphState(TypedDict):
    """The state of the FounderMode research graph."""
    query: str
    plan: ResearchPlan
    facts: Annotated[List[ResearchFact], add]
    draft: InvestmentMemo
    messages: Annotated[List[BaseMessage], add]
