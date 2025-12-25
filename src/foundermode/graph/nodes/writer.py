from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from foundermode.config import settings
from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import FounderState

# Define the prompt
writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a Partner at Sequoia Capital writing a Final Investment Committee Memo.

    Objective: Synthesize the provided research facts into a rigorous, skeptical, and data-backed investment thesis.

    Research Subject: {research_question}

    [MANDATORY RULES]
    1. **Cite Everything:** Every claim must be followed by a citation from the provided facts
       (e.g., "Market is growing at 5% (Gartner, 2023)").
    2. **No Fluff:** Do not use adjectives like "revolutionary" or "cutting-edge". Use numbers.
    3. **Structure:**
       - **Executive Summary:** Bottom Line Up Front (BLUF). Recommendation (Invest/Pass) + top 3 reasons.
       - **Market Analysis:** TAM/SAM, CAGR, and "Why Now?".
       - **Competitive Landscape:** Direct & Indirect competitors. What is the Moat?
         (Network effects, Switching costs, etc.)

    [Input Data]
    {research_facts}
    """,
        ),
    ]
)


def get_writer_chain() -> Any:
    if not settings.openai_api_key:
        return None

    llm = ChatOpenAI(model=settings.model_name, temperature=0, openai_api_key=settings.openai_api_key)
    return writer_prompt | llm.with_structured_output(InvestmentMemo)


# For backward compatibility
writer_chain = get_writer_chain()


def writer_node(state: FounderState) -> dict[str, Any]:
    """
    Synthesizes the investment memo.
    Supports dynamic fallback to mock data if OpenAI key is missing.
    """
    # 1. Attempt Live Logic
    chain = get_writer_chain()
    if chain:
        try:
            # Format facts
            facts_str = (
                "\n".join([f"- {f.content} (Source: {f.source})" for f in state["research_facts"]])
                if state["research_facts"]
                else "No facts collected."
            )

            memo = chain.invoke({"research_question": state["research_question"], "research_facts": facts_str})
            return {"memo_draft": memo, "next_step": "finish"}
        except Exception as e:
            print(f"Writer LLM call failed, falling back to mock: {e}")

    # 2. Mock Fallback Logic
    memo = InvestmentMemo(
        executive_summary=(
            f"Mock Executive Summary for {state['research_question']}. "
            "The concept shows significant potential based on early indicators."
        ),
        market_analysis=(
            "The market is currently undergoing rapid digital transformation, "
            "creating a vacuum for innovative solutions."
        ),
        competitive_landscape=(
            "While established players exist, there is a clear gap in the mid-market segment "
            "that this proposal addresses."
        ),
    )

    return {"memo_draft": memo, "next_step": "finish"}
