import os

from dotenv import load_dotenv
from langsmith import Client

load_dotenv()


def create_benchmark_dataset() -> None:
    client = Client()
    dataset_name = "FounderMode Benchmark v1"

    # Check if dataset exists
    if client.has_dataset(dataset_name=dataset_name):
        print(f"Dataset '{dataset_name}' already exists.")
        return

    dataset = client.create_dataset(
        dataset_name=dataset_name, description="Diverse business ideas for evaluating FounderMode agent performance."
    )

    examples = [
        {
            "inputs": {"research_question": "Uber for Dog Walking"},
            "outputs": {},  # We evaluate the generated memo against rubrics, no ground truth string required yet
        },
        {
            "inputs": {"research_question": "B2B SaaS for Construction Management"},
            "outputs": {},
        },
        {
            "inputs": {"research_question": "AI-Powered Personal Stylist"},
            "outputs": {},
        },
        {
            "inputs": {"research_question": "Drone Delivery for Medical Supplies in Rural Areas"},
            "outputs": {},
        },
        {
            "inputs": {"research_question": "Subscription Box for Rare Coffee"},
            "outputs": {},
        },
    ]

    client.create_examples(
        inputs=[e["inputs"] for e in examples],
        outputs=[e["outputs"] for e in examples],
        dataset_id=dataset.id,
    )

    print(f"Successfully created dataset '{dataset_name}' with {len(examples)} examples.")


if __name__ == "__main__":
    if not os.environ.get("LANGCHAIN_API_KEY"):
        print("Error: LANGCHAIN_API_KEY environment variable not found.")
    else:
        create_benchmark_dataset()
