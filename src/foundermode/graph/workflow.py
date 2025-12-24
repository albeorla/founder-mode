from typing import List, TypedDict, Annotated
from operator import add

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END

from foundermode.domain.schema import ResearchPlan, ResearchFact, InvestmentMemo
from foundermode.domain.state import GraphState
from foundermode.graph.nodes.mock import mock_analyst

def create_workflow() -> StateGraph:
    """Creates the LangGraph workflow."""
    workflow = StateGraph(GraphState)
    
    workflow.add_node("analyst", mock_analyst)
    
    # Define the graph edges
    workflow.set_entry_point("analyst")
    workflow.add_edge("analyst", END)
    
    return workflow
