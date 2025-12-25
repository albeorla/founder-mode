import logging
from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from foundermode.config import settings
from foundermode.domain.schema import CriticVerdict
from foundermode.domain.state import FounderState

logger = logging.getLogger(__name__)

# Define the prompt for the Critic Node
critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a Skeptical Managing Partner at a top-tier Venture Capital firm.
    Your job is to ruthlessly critique the Investment Memo provided by your associate.

    [YOUR CRITERIA]
    1. **Quantitative Rigor:** Does the memo include specific numbers for CAC, LTV, Churn, and TAM/SAM?
       If it uses terms like \"large market\" or \"efficient acquisition\" without numbers, REJECT it.
    2. **Citation Quality:** Are the claims backed by the research logs?
       If it makes wild claims or uses \"Mock Data\" as a primary source, REJECT it.
    3. **Analytical Depth:** Does it identify concrete risks/killers or just summarize the product?

    [VERDICT RULES]
    - 'reject': If the memo is generic, lacks numbers, or has weak citations.
    - 'approve': Only if the memo is data-heavy, cited, and provides a deep strategic analysis.

    [INPUT DATA]
    Research logs:
    {research_facts}
    """,
        ),
        (
            "human",
            "Please review this Investment Memo and provide your verdict:\n\n{memo_draft}",
        ),
    ]
)


def get_critic_chain() -> Any:
    """Initialize the LLM chain for the critic node with structured output."""
    if not settings.openai_api_key:
        return None

    llm = ChatOpenAI(
        model=settings.model_name,
        temperature=0,
        openai_api_key=settings.openai_api_key,
    )
    return critic_prompt | llm.with_structured_output(CriticVerdict)


def critic_node(state: FounderState) -> dict[str, Any]:
    """
    Analyzes the investment memo and provides a verdict.
    """
    logger.info("Critic Node: Starting analysis.")
    logger.debug(f"Revision count: {state.get('revision_count', 0)}")

    # 1. Attempt Live Logic
    chain = get_critic_chain()
    if chain:
        try:
            # Format facts for context
            facts_str = (
                "\n".join([f"- {f.content} (Source: {f.source})" for f in state["research_facts"]])
                if state["research_facts"]
                else "No facts collected."
            )

            # Format memo for review
            memo = state["memo_draft"]
            memo_str = (
                f"EXECUTIVE SUMMARY:\n{memo.executive_summary}\n\n"
                f"MARKET ANALYSIS:\n{memo.market_analysis}\n\n"
                f"COMPETITIVE LANDSCAPE:\n{memo.competitive_landscape}"
            )

            logger.debug("Invoking Critic LLM.")
            verdict = chain.invoke({"research_facts": facts_str, "memo_draft": memo_str})

            logger.info(f"Critic Verdict: {verdict.action}")
            logger.debug(f"Critic Feedback: {verdict.feedback}")

            # Update state: Append feedback to history and increment revision count
            return {
                "critique_history": [verdict.feedback],
                "revision_count": state.get("revision_count", 0) + (1 if verdict.action == "reject" else 0),
                "next_step": verdict.action,
            }
        except Exception as e:
            logger.error(f"Critic LLM call failed: {e}", exc_info=True)
            # Fallback on error: assume rejection if we can't decide, to be safe
            return {
                "critique_history": [f"Critic Error: {str(e)}. Defaulting to rejection for safety."],
                "revision_count": state.get("revision_count", 0) + 1,
                "next_step": "reject",
            }

    # 2. Mock Fallback Logic (if no API key)
    logger.warning("Critic Node: No API key found. Using mock logic.")
    # For testing/dev: if executive summary contains "Mock", we reject it to demonstrate the loop
    is_mock = "Mock" in state["memo_draft"].executive_summary
    action = "reject" if is_mock else "approve"

    return {
        "critique_history": ["Mock Critique: This memo looks like a placeholder." if is_mock else "Mock Approval."],
        "revision_count": state.get("revision_count", 0) + (1 if is_mock else 0),
        "next_step": action,
    }
