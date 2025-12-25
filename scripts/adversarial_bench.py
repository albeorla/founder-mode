import asyncio
import os
from typing import Any

from langsmith import Client, evaluate

from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import FounderState
from foundermode.graph.workflow import create_workflow


def create_adversarial_dataset() -> None:
    client = Client()
    dataset_name = "FounderMode Adversarial v1"

    if client.has_dataset(dataset_name=dataset_name):
        return

    dataset = client.create_dataset(
        dataset_name=dataset_name, description="Deliberately weak or fluffy business ideas to test the Critic node."
    )

    examples = [
        {
            "inputs": {"research_question": "A generic blockchain for cats"},
            "outputs": {},
        },
        {
            "inputs": {"research_question": "A lifestyle business with no scale"},
            "outputs": {},
        },
        {
            "inputs": {"research_question": "A product that already has 1000 identical competitors"},
            "outputs": {},
        },
    ]

    client.create_examples(
        inputs=[e["inputs"] for e in examples],
        outputs=[e["outputs"] for e in examples],
        dataset_id=dataset.id,
    )
    print(f"Created adversarial dataset '{dataset_name}'")


async def run_adversarial_bench() -> None:
    # Define target function: Run the graph and return the final state
    def target(inputs: dict[str, Any]) -> dict[str, Any]:
        app = create_workflow()
        initial_state: FounderState = {
            "research_question": inputs["research_question"],
            "research_facts": [],
            "memo_draft": InvestmentMemo(),
            "messages": [],
            "next_step": "init",
            "research_topic": None,
            "critique_history": [],
            "revision_count": 0,
        }
        final_state = app.invoke(initial_state)
        return final_state  # type: ignore

    # Evaluator: Check if the critic was triggered (revision_count > 0)
    def critic_triggered_evaluator(run: Any, example: Any) -> dict[str, Any]:
        revision_count = run.outputs.get("revision_count", 0)
        return {
            "key": "critic_triggered",
            "score": 1 if revision_count > 0 else 0,
            "comment": f"Revision count: {revision_count}",
        }

    # Run evaluation
    results = evaluate(
        target,
        data="FounderMode Adversarial v1",
        evaluators=[critic_triggered_evaluator],
        experiment_prefix="adversarial-red-team",
    )
    print(results)


if __name__ == "__main__":
    if not os.environ.get("LANGCHAIN_API_KEY"):
        print("Skipping adversarial bench: LANGCHAIN_API_KEY not found.")
    else:
        create_adversarial_dataset()
        asyncio.run(run_adversarial_bench())
