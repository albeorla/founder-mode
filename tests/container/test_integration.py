import os

import pytest

from foundermode.domain.schema import InvestmentMemo
from foundermode.domain.state import FounderState
from foundermode.graph.nodes.researcher import researcher_node
from foundermode.memory.vector_store import ChromaManager


def test_researcher_node_execution_in_container() -> None:
    """Verify that the researcher node can execute search and scrape inside the container."""
    state: FounderState = {
        "research_question": "Stripe pricing model",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "init",
        "research_topic": "Stripe pricing model",
        "critique_history": [],
        "revision_count": 0,
    }

    try:
        result = researcher_node(state)
        assert "research_facts" in result
        assert result["next_step"] == "planner"
    except Exception as e:
        pytest.fail(f"Researcher node failed in container: {e}")


def test_chromadb_persistence_in_container() -> None:
    """Verify that ChromaDB can write to the persistent volume."""
    import shutil

    persist_dir = "./.chroma_db_container_test"
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    manager = ChromaManager(persist_directory=persist_dir)

    from foundermode.domain.schema import ResearchFact

    fact = ResearchFact(content="Container persistence test", source="container")

    success = manager.add_facts([fact])
    assert success is True

    # Verify file exists in persist_dir
    assert os.path.exists(persist_dir)
    assert len(os.listdir(persist_dir)) > 0
