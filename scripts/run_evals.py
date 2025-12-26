import os
from typing import Any

from langsmith import evaluate

from foundermode.domain.schema import InvestmentMemo
from foundermode.evaluation.evaluators import (
    HallucinationEvaluator,
    InvestorRubricEvaluator,
    PlannerEvaluator,
    ResearcherEvaluator,
    RevisionDeltaEvaluator,
)
from foundermode.graph.workflow import create_workflow


def run_evals() -> None:
    # Define target function (wrap the graph)
    def target(inputs: dict[str, Any]) -> dict[str, Any]:
        app = create_workflow()
        initial_state = {
            "research_question": inputs["research_question"],
            "research_facts": [],
            "memo_draft": InvestmentMemo(),
            "messages": [],
            "next_step": "init",
            "research_topic": None,
            "revision_count": 0,
            "critique_history": [],
        }
        # Run graph
        final_state = app.invoke(initial_state)
        return final_state  # type: ignore

    # Define evaluators
    evaluators = [
        InvestorRubricEvaluator(),
        PlannerEvaluator(),
        ResearcherEvaluator(),
        RevisionDeltaEvaluator(),
        HallucinationEvaluator(),
    ]

    # Run evaluation
    results = evaluate(
        target,
        data="FounderMode Benchmark v2",
        evaluators=evaluators,
        experiment_prefix="foundermode-v2-enhanced",
        max_concurrency=2,
    )

    print(results)


if __name__ == "__main__":
    if not os.environ.get("LANGCHAIN_API_KEY"):
        print("Skipping LangSmith evaluation: LANGCHAIN_API_KEY not found.")
    else:
        run_evals()
