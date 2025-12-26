from typing import cast
from unittest.mock import MagicMock, patch

import pytest

from foundermode.domain.schema import ResearchFact
from foundermode.memory.vector_store import ChromaManager


@pytest.fixture
def chroma_manager() -> ChromaManager:
    # Patch ChromaVectorStore class to return a mock instance
    with patch("foundermode.memory.vector_store.ChromaVectorStore"):
        manager = ChromaManager(persist_directory=".tmp_chroma")
        # manager.store is now a MagicMock (instance of MockStore)
        return manager


def test_initialization(chroma_manager: ChromaManager) -> None:
    assert chroma_manager is not None
    assert chroma_manager.store is not None


def test_add_facts(chroma_manager: ChromaManager) -> None:
    facts = [
        ResearchFact(content="The market for AI is growing.", source="TechCrunch", relevance_score=0.9),
        ResearchFact(content="Competitor X raised $5M.", source="VentureBeat", relevance_score=0.8),
    ]

    success = chroma_manager.add_facts(facts)
    assert success is True

    store_mock = cast(MagicMock, chroma_manager.store)
    assert store_mock.add_texts.called

    # Verify call arguments
    call_args = store_mock.add_texts.call_args
    assert len(call_args.kwargs["texts"]) == 2
    assert len(call_args.kwargs["metadatas"]) == 2
    assert len(call_args.kwargs["ids"]) == 2


def test_query_similar(chroma_manager: ChromaManager) -> None:
    # Mock store query
    store_mock = cast(MagicMock, chroma_manager.store)
    store_mock.query.return_value = [
        {"content": "Fact 1", "metadata": {"source": "S1", "relevance_score": 0.9}},
        {"content": "Fact 2", "metadata": {"source": "S2", "relevance_score": 0.8}},
    ]

    results = chroma_manager.query_similar("test query", k=2)

    assert len(results) == 2
    assert results[0].content == "Fact 1"
    assert results[0].source == "S1"


def test_vector_store_integration() -> None:
    # Test interaction with the store mock
    with patch("foundermode.memory.vector_store.ChromaVectorStore"):
        manager = ChromaManager(persist_directory=".tmp_integration")
        fact = ResearchFact(content="Integration test", source="pytest")

        manager.add_facts([fact])
        store_mock = cast(MagicMock, manager.store)
        assert store_mock.add_texts.called

        manager.query_similar("search")
        assert store_mock.query.called


def test_add_scraped_text(chroma_manager: ChromaManager) -> None:
    url = "https://example.com/long"
    long_text = "Word " * 500  # Should result in multiple chunks

    success = chroma_manager.add_scraped_text(url, long_text)

    assert success is True
    store_mock = cast(MagicMock, chroma_manager.store)
    assert store_mock.add_texts.called

    call_args = store_mock.add_texts.call_args
    texts = call_args.kwargs["texts"]
    metadatas = call_args.kwargs["metadatas"]
    ids = call_args.kwargs["ids"]

    # Verify chunks
    assert len(texts) > 1
    assert len(metadatas) == len(texts)
    assert len(ids) == len(texts)

    # Verify metadata contains source and chunk index
    assert metadatas[0]["source"] == url
    assert "chunk" in metadatas[0]
