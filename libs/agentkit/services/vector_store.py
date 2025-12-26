import hashlib
import logging
from typing import Any, Protocol, cast

logger = logging.getLogger("agentkit.services.vector_store")


class VectorStore(Protocol):
    """Protocol for vector store implementations."""

    def add_texts(
        self, texts: list[str], metadatas: list[dict[str, Any]] | None = None, ids: list[str] | None = None
    ) -> bool: ...
    def query(self, query: str, k: int = 3) -> list[dict[str, Any]]: ...


class InMemoryVectorStore:
    """Simple in-memory vector store for testing (no real embeddings, just keyword match)."""

    def __init__(self) -> None:
        self.data: list[dict[str, Any]] = []

    def add_texts(
        self, texts: list[str], metadatas: list[dict[str, Any]] | None = None, ids: list[str] | None = None
    ) -> bool:
        for i, text in enumerate(texts):
            meta = metadatas[i] if metadatas else {}
            item_id = ids[i] if ids else hashlib.md5(text.encode()).hexdigest()
            self.data.append({"id": item_id, "content": text, "metadata": meta})
        return True

    def query(self, query: str, k: int = 3) -> list[dict[str, Any]]:
        # Extremely simple keyword search for testing
        query_words = set(query.lower().split())
        scored = []
        for item in self.data:
            content_words = set(item["content"].lower().split())
            score = len(query_words.intersection(content_words))
            scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for score, item in scored[:k] if score > 0]


class ChromaVectorStore:
    """Vector store implementation using ChromaDB (Lazy Import)."""

    def __init__(self, persist_directory: str, collection_name: str = "agentkit"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self._collection: Any = None

    def _get_collection(self) -> Any:
        if self._collection is None:
            import chromadb

            client = chromadb.PersistentClient(path=self.persist_directory)
            # Default embedding function for now
            self._collection = client.get_or_create_collection(name=self.collection_name)
        return self._collection

    def add_texts(
        self, texts: list[str], metadatas: list[dict[str, Any]] | None = None, ids: list[str] | None = None
    ) -> bool:
        try:
            collection = self._get_collection()
            if ids is None:
                ids = [hashlib.md5(t.encode()).hexdigest() for t in texts]
            collection.upsert(documents=texts, metadatas=cast(Any, metadatas), ids=ids)
            return True
        except Exception as e:
            logger.error(f"Chroma add_texts failed: {e}")
            return False

    def query(self, query: str, k: int = 3) -> list[dict[str, Any]]:
        try:
            collection = self._get_collection()
            if collection.count() == 0:
                return []

            results = collection.query(query_texts=[query], n_results=k)
            output = []
            if results["documents"]:
                docs = results["documents"][0]
                metas = results["metadatas"][0] if results["metadatas"] else [{}] * len(docs)
                ids = results["ids"][0]
                for i in range(len(docs)):
                    output.append({"id": ids[i], "content": docs[i], "metadata": metas[i]})
            return output
        except Exception as e:
            logger.error(f"Chroma query failed: {e}")
            return []
