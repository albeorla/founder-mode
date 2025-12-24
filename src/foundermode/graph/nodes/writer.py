from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import FounderState

# Define the prompt
writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a Senior Investment Analyst at a top-tier VC firm.
    Your goal is to write a comprehensive Investment Memo based on the collected research.

    Research Question: {research_question}

    Collected Facts:
    {research_facts}

    Write the following sections:
    1. Executive Summary (BLUF)
    2. Market Analysis
    3. Competitive Landscape

    Be objective, data-driven, and concise.""",
        ),
    ]
)

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Create structured chain
# We want to output an InvestmentMemo object directly.
writer_chain = writer_prompt | llm.with_structured_output(InvestmentMemo)


def writer_node(state: FounderState) -> dict[str, Any]:
    """
    Synthesizes the investment memo.
    """
    # Format facts
    facts_str = (
        "\n".join([f"- {f.content} (Source: {f.source})" for f in state["research_facts"]])
        if state["research_facts"]
        else "No facts collected."
    )

    memo = writer_chain.invoke({"research_question": state["research_question"], "research_facts": facts_str})

    return {"memo_draft": memo, "next_step": "finish"}
