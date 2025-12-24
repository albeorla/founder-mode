from typing import Any, Literal, TypedDict

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from foundermode.config import settings
from foundermode.domain.state import FounderState


class PlannerOutput(TypedDict):
    action: Literal["research", "write"]
    research_topic: str | None
    reason: str


# Define the prompt
planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are the Lead Strategist for a Venture Capital due diligence agent.
    Your goal is to decide the next step in the research process.

    Current Task: {research_question}

    Key Facts Collected:
    {research_facts}

    Decide whether to:
    1. 'research': If you need more information. Provide a specific 'research_topic' to search for.
    2. 'write': If you have sufficient information. 'research_topic' should be None.

    Provide a reason for your decision.""",
        ),
    ]
)


# Initialize LLM lazily to avoid error if API key is missing at import time
def get_planner_chain() -> Any:
    if not settings.openai_api_key:
        return None

    llm = ChatOpenAI(model=settings.model_name, temperature=0, openai_api_key=settings.openai_api_key)
    return planner_prompt | llm.with_structured_output(PlannerOutput)


# For backward compatibility and patching in tests
planner_chain = get_planner_chain()


def planner_node(state: FounderState) -> dict[str, Any]:
    """
    Decides the next step based on the current state.
    Supports dynamic fallback to mock data if OpenAI key is missing.
    """
    # 1. Attempt Live Logic
    chain = get_planner_chain()
    if chain:
        try:
            # Format facts for prompt
            facts_str = (
                "\n".join([f"- {f.content}" for f in state["research_facts"]])
                if state["research_facts"]
                else "No facts collected yet."
            )

            result = chain.invoke({"research_question": state["research_question"], "research_facts": facts_str})
            return {"next_step": result["action"], "research_topic": result.get("research_topic")}
        except Exception as e:
            # Fallback on error
            print(f"Planner LLM call failed, falling back to mock: {e}")

    # 2. Mock Fallback Logic
    # Simple heuristic: if we have fewer than 3 facts, keep researching.
    if len(state["research_facts"]) < 3:
        # Generate a mock topic based on the question if none exists
        mock_topics = ["Market size", "Competitor analysis", "Pricing strategy"]
        topic_idx = len(state["research_facts"]) % len(mock_topics)
        return {"next_step": "research", "research_topic": f"{mock_topics[topic_idx]} for {state['research_question']}"}

    return {"next_step": "write", "research_topic": None}
