from agentkit.services.vector_store import InMemoryVectorStore


def test_in_memory_vector_store() -> None:
    store = InMemoryVectorStore()
    store.add_texts(
        texts=["The sky is blue", "The grass is green"],
        metadatas=[{"color": "blue"}, {"color": "green"}],
        ids=["1", "2"],
    )

    results = store.query("Something blue", k=1)
    assert len(results) == 1
    assert "sky" in results[0]["content"]
    assert results[0]["metadata"]["color"] == "blue"


def test_in_memory_vector_store_empty() -> None:
    store = InMemoryVectorStore()
    results = store.query("Anything", k=1)
    assert results == []
