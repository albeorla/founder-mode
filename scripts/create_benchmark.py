import os

from dotenv import load_dotenv
from langsmith import Client

load_dotenv()


def create_benchmark_dataset() -> None:
    client = Client()
    dataset_name = "FounderMode Benchmark v2"

    # Check if dataset exists
    if client.has_dataset(dataset_name=dataset_name):
        print(f"Dataset '{dataset_name}' already exists.")
        return

    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="Diverse business ideas for evaluating FounderMode agent performance (v2).",
    )

    examples = [
        # Easy (Consumer)
        {"inputs": {"research_question": "Uber for Dog Walking"}, "outputs": {}},
        {"inputs": {"research_question": "Subscription Box for Rare Coffee"}, "outputs": {}},
        {"inputs": {"research_question": "AI-Powered Personal Stylist"}, "outputs": {}},
        {"inputs": {"research_question": "Peloton for Rowing"}, "outputs": {}},
        {"inputs": {"research_question": "Marketplace for used high-end camera gear"}, "outputs": {}},
        # Hard (Niche B2B)
        {"inputs": {"research_question": "B2B SaaS for Construction Management"}, "outputs": {}},
        {
            "inputs": {
                "research_question": "Predictive maintenance software for semiconductor manufacturing equipment"
            },
            "outputs": {},
        },
        {
            "inputs": {
                "research_question": ("AI-driven logistics optimization for cold-chain pharmaceutical shipping")
            },
            "outputs": {},
        },
        {
            "inputs": {
                "research_question": ("Compliance automation platform for European medical device manufacturers (MDR)")
            },
            "outputs": {},
        },
        {
            "inputs": {
                "research_question": ("ERP system specifically designed for boutique vertical farming operations")
            },
            "outputs": {},
        },
        # Trap (Physics/Logic violations)
        {
            "inputs": {"research_question": ("Perpetual motion machine based on magnetic levitation for home energy")},
            "outputs": {},
        },
        {
            "inputs": {
                "research_question": (
                    "FTL (Faster Than Light) communication device using quantum entanglement for deep space"
                )
            },
            "outputs": {},
        },
        {
            "inputs": {"research_question": "Water-powered car conversion kit using onboard electrolysis"},
            "outputs": {},
        },
        {
            "inputs": {
                "research_question": ("100% efficient solar panels that work in total darkness using 'dark energy'")
            },
            "outputs": {},
        },
        {
            "inputs": {"research_question": "Cold fusion reactor small enough to power a smartphone"},
            "outputs": {},
        },
        # Adversarial (No-business-model fluff)
        {
            "inputs": {
                "research_question": ("A decentralized platform for sharing digital high-fives on the blockchain")
            },
            "outputs": {},
        },
        {
            "inputs": {"research_question": "An app that lets you smell the color blue using generative AI"},
            "outputs": {},
        },
        {
            "inputs": {
                "research_question": ("A subscription service for monthly 'positive vibes' sent via ultrasonic waves")
            },
            "outputs": {},
        },
        {
            "inputs": {"research_question": "A social network exclusively for people who own left-handed pens"},
            "outputs": {},
        },
        {
            "inputs": {
                "research_question": (
                    "A cloud-based solution for digitizing physical rocks into NFTs for 'pet rock 2.0'"
                )
            },
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
