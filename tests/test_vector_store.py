import os
import shutil
from collections.abc import Generator
from unittest.mock import MagicMock

import pytest

from foundermode.domain.schema import ResearchFact
from foundermode.memory.vector_store import ChromaManager

# Use a temporary directory for the vector store in tests
TEST_DB_DIR = ".test_chroma_db"


@pytest.fixture  # type: ignore
def chroma_manager() -> Generator[ChromaManager, None, None]:
    # Setup
    manager = ChromaManager(persist_directory=TEST_DB_DIR)
    yield manager
    # Teardown: Remove the test database directory
    if os.path.exists(TEST_DB_DIR):
        shutil.rmtree(TEST_DB_DIR)


def test_initialization(chroma_manager: ChromaManager) -> None:
    assert chroma_manager.client is not None

    assert chroma_manager.collection is not None


def test_add_facts(chroma_manager: ChromaManager) -> None:
    facts = [
        ResearchFact(content="The market for AI is growing.", source="TechCrunch", relevance_score=0.9),
        ResearchFact(content="Competitor X raised $5M.", source="VentureBeat", relevance_score=0.8),
    ]

    # We mock the actual adding to avoid needing a real OpenAI key for embeddings during this unit test
    # However, since we are using ChromaManager which likely initializes embeddings, we might need to mock that.

    # For this test, let's assume we can mock the collection methods
    chroma_manager.collection = MagicMock()

    success = chroma_manager.add_facts(facts)
    assert success is True
    assert chroma_manager.collection.add.called

    # Verify call arguments
    call_args = chroma_manager.collection.add.call_args
    assert len(call_args.kwargs["documents"]) == 2
    assert len(call_args.kwargs["metadatas"]) == 2
    assert len(call_args.kwargs["ids"]) == 2

    assert call_args.kwargs["documents"][0] == "The market for AI is growing."
    assert call_args.kwargs["metadatas"][0]["source"] == "TechCrunch"


def test_query_similar(chroma_manager: ChromaManager) -> None:
    # Mock collection query
    chroma_manager.collection = MagicMock()
    chroma_manager.collection.query.return_value = {
        "documents": [["The market for AI is growing."]],
        "metadatas": [[{"source": "TechCrunch", "relevance_score": 0.9}]],
        "distances": [[0.1]],
    }

    results = chroma_manager.query_similar("market growth", k=1)

    assert len(results) == 1
    assert isinstance(results[0], ResearchFact)
    assert results[0].content == "The market for AI is growing."
    assert results[0].source == "TechCrunch"


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")  # type: ignore
def test_vector_store_integration() -> None:
    # Use a unique collection for integration test
    persist_dir = ".test_chroma_db_integration"
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    manager = ChromaManager(persist_directory=persist_dir, collection_name="integration_test")
    try:
        facts = [
            ResearchFact(
                content="Apple makes the iPhone.",
                source="Apple",
                relevance_score=1.0,
                title="Apple Products",
            ),
            ResearchFact(
                content="Tesla makes electric cars.",
                source="Tesla",
                relevance_score=1.0,
                title="Tesla Products",
            ),
        ]

        # Add facts
        manager.add_facts(facts)

        # Query
        results = manager.query_similar("Which company makes phones?", k=1)

        assert len(results) == 1
        assert "Apple" in results[0].content
        assert results[0].source == "Apple"

    finally:
        if os.path.exists(persist_dir):
            shutil.rmtree(persist_dir)
