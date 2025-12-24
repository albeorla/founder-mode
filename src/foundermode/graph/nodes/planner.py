from typing import Any, Literal, TypedDict

from foundermode.domain.state import FounderState
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class PlannerOutput(TypedDict):
    action: Literal["research", "write"]
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
    1. 'research': If you need more information to answer the question comprehensively.
    2. 'write': If you have sufficient information to draft the investment memo.

    Provide a reason for your decision.""",
        ),
    ]
)

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Create structured chain
planner_chain = planner_prompt | llm.with_structured_output(PlannerOutput)


def planner_node(state: FounderState) -> dict[str, Any]:
    """
    Decides the next step based on the current state.
    """
    # Format facts for prompt
    facts_str = (
        "\n".join([f"- {f.content}" for f in state["research_facts"]])
        if state["research_facts"]
        else "No facts collected yet."
    )

    result = planner_chain.invoke({"research_question": state["research_question"], "research_facts": facts_str})

    return {"next_step": result["action"]}
