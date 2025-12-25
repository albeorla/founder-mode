import logging
from typing import Any, Literal, TypedDict

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from foundermode.config import settings
from foundermode.domain.state import FounderState

logger = logging.getLogger(__name__)


class PlannerOutput(TypedDict):
    action: Literal["research", "write"]
    research_topic: str | None
    reason: str


# Define the prompt
planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a Senior Investment Strategist at a top-tier VC firm.
    Your goal is to rigorously validate a startup idea by orchestrating a deep research process.

    Current Investment Thesis/Idea: {research_question}

    Key Facts Collected So Far:
    {research_facts}

    Your Mandate:
    - Prioritize "Hard Truths": Unit Economics (CAC, LTV), Market Size (TAM/SAM), and Incumbent Moats.
    - Ignore generic fluff. We need specific numbers and competitor names.
    - If key financial or competitive data is missing, you MUST choose 'research'.
    - Only choose 'write' when you have enough evidence to write a 10-page committee memo.

    Decide next step:
    1. 'research': Provide a specific, targeted search query
       (e.g., "Uber customer acquisition cost 2014", "Toast POS churn rate").
    2. 'write': If you have sufficient high-signal data.

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
    logger.info("Planner Node: Starting execution.")
    logger.debug(
        f"Planner Input State: facts_count={len(state['research_facts'])}, " f"topic={state.get('research_topic')}"
    )

    # 1. Attempt Live Logic
    chain = get_planner_chain()

    # Safety Check: Limit total facts to prevent infinite loops
    MAX_FACTS = 15  # Approx 5 loops of 3 facts
    if len(state["research_facts"]) >= MAX_FACTS:
        logger.warning(f"Planner: Reached MAX_FACTS ({MAX_FACTS}). Forcing 'write' transition.")
        return {"next_step": "write", "research_topic": None}

    if chain:
        try:
            # Format facts for prompt
            facts_str = (
                "\n".join([f"- {f.content}" for f in state["research_facts"]])
                if state["research_facts"]
                else "No facts collected yet."
            )

            logger.debug(f"Invoking Planner LLM with {len(state['research_facts'])} facts.")
            result = chain.invoke({"research_question": state["research_question"], "research_facts": facts_str})
            logger.info(f"Planner Decision: {result['action']} (Topic: {result.get('research_topic')})")
            logger.debug(f"Planner Reasoning: {result.get('reason')}")

            return {"next_step": result["action"], "research_topic": result.get("research_topic")}
        except Exception as e:
            # Fallback on error
            logger.error(f"Planner LLM call failed, falling back to mock: {e}", exc_info=True)
            print(f"Planner LLM call failed, falling back to mock: {e}")

    # 2. Mock Fallback Logic
    # Simple heuristic: if we have fewer than 3 facts, keep researching.
    logger.info("Planner Node: Using Mock Fallback Logic.")
    if len(state["research_facts"]) < 3:
        # Generate a mock topic based on the question if none exists
        mock_topics = ["Market size", "Competitor analysis", "Pricing strategy"]
        topic_idx = len(state["research_facts"]) % len(mock_topics)
        topic = f"{mock_topics[topic_idx]} for {state['research_question']}"
        logger.info(f"Mock Planner: Decided 'research' on '{topic}'.")
        return {"next_step": "research", "research_topic": topic}

    logger.info("Mock Planner: Decided 'write'.")
    return {"next_step": "write", "research_topic": None}
