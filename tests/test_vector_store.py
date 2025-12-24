from unittest.mock import MagicMock, patch

import pytest

from foundermode.domain.schema import ResearchFact
from foundermode.memory.vector_store import ChromaManager


@pytest.fixture
def chroma_manager() -> ChromaManager:
    # Use a temporary directory for the vector store during tests
    with patch("foundermode.memory.vector_store.chromadb.PersistentClient") as mock_client:
        # Mock the collection
        mock_collection = MagicMock()
        mock_client.return_value.get_or_create_collection.return_value = mock_collection
        manager = ChromaManager(persist_directory=".tmp_chroma")
        return manager


def test_initialization(chroma_manager: ChromaManager) -> None:
    assert chroma_manager is not None
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
    assert chroma_manager.collection.upsert.called

    # Verify call arguments
    call_args = chroma_manager.collection.upsert.call_args
    assert len(call_args.kwargs["documents"]) == 2
    assert len(call_args.kwargs["metadatas"]) == 2
    assert len(call_args.kwargs["ids"]) == 2


def test_query_similar(chroma_manager: ChromaManager) -> None:
    # Mock collection query
    chroma_manager.collection.query.return_value = {
        "documents": [["Fact 1", "Fact 2"]],
        "metadatas": [[{"source": "S1", "relevance_score": 0.9}, {"source": "S2", "relevance_score": 0.8}]],
        "ids": [["id1", "id2"]],
        "distances": [[0.1, 0.2]],
    }

    results = chroma_manager.query_similar("test query", k=2)

    assert len(results) == 2
    assert results[0].content == "Fact 1"
    assert results[0].source == "S1"


def test_vector_store_integration() -> None:
    # Integration test with real (but local) ChromaDB if possible
    # For now, we mock the PersistentClient but test the manager logic
    with patch("foundermode.memory.vector_store.chromadb.PersistentClient") as mock_client:
        mock_coll = MagicMock()
        mock_client.return_value.get_or_create_collection.return_value = mock_coll

        manager = ChromaManager(persist_directory=".tmp_integration")
        fact = ResearchFact(content="Integration test", source="pytest")

        manager.add_facts([fact])
        assert mock_coll.upsert.called

        manager.query_similar("search")
        assert mock_coll.query.called
