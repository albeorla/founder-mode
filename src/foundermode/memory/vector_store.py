import hashlib
from typing import Any, cast

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from chromadb.utils import embedding_functions
from langchain_openai import OpenAIEmbeddings

from foundermode.config import settings
from foundermode.domain.schema import ResearchFact


class ChromaLangChainAdapter(EmbeddingFunction[Documents]):  # type: ignore
    def __init__(self, langchain_embeddings: Any) -> None:
        self._langchain_embeddings = langchain_embeddings

    def __call__(self, input: Documents) -> Embeddings:
        return cast(Embeddings, self._langchain_embeddings.embed_documents(input))


class ChromaManager:
    def __init__(self, persist_directory: str | None = None, collection_name: str = "founder_mode_memory") -> None:
        path = persist_directory or settings.chroma_db_path
        self.client = chromadb.PersistentClient(path=path)

        # Use settings for API key
        api_key = settings.openai_api_key
        self.embedding_fn: EmbeddingFunction[Any]
        if api_key:
            langchain_emb = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key)
            self.embedding_fn = ChromaLangChainAdapter(langchain_emb)
        else:
            # Fallback for tests if no key is present
            self.embedding_fn = cast(EmbeddingFunction[Any], embedding_functions.DefaultEmbeddingFunction())

        self.collection = self.client.get_or_create_collection(
            name=collection_name, embedding_function=cast(Any, self.embedding_fn)
        )

    def _generate_id(self, fact: ResearchFact) -> str:
        """Generate a deterministic ID for a fact to prevent duplicates."""
        # Prefer source URL as a stable identifier
        if fact.source and fact.source.startswith("http"):
            return hashlib.md5(fact.source.encode()).hexdigest()
        # Fallback to content hash
        return hashlib.md5(fact.content.encode()).hexdigest()

    def add_facts(self, facts: list[ResearchFact]) -> bool:
        if not facts:
            return True

        # Deduplicate facts within the input list by ID
        unique_facts = {}
        for f in facts:
            fact_id = self._generate_id(f)
            unique_facts[fact_id] = f

        facts = list(unique_facts.values())

        documents = [f.content for f in facts]
        metadatas = [
            cast(
                dict[str, Any],
                {"source": f.source, "title": f.title or "", "relevance_score": f.relevance_score or 0.0},
            )
            for f in facts
        ]
        ids = [self._generate_id(f) for f in facts]

        try:
            # Use upsert to handle existing IDs gracefully
            self.collection.upsert(documents=documents, metadatas=cast(Any, metadatas), ids=ids)
            return True
        except Exception as e:
            print(f"Error adding facts: {e}")
            return False

    def query_similar(self, query: str, k: int = 3) -> list[ResearchFact]:
        # Optimization: Only query if collection has items
        if self.collection.count() == 0:
            return []

        results = self.collection.query(query_texts=[query], n_results=k)

        facts = []
        if results["documents"]:
            # results is a dict of lists of lists (batch queries)
            # We queried one text, so we take index 0
            docs = results["documents"][0]
            metas = results["metadatas"][0] if results["metadatas"] else None

            if docs and metas:
                for i in range(len(docs)):
                    content = docs[i]
                    meta = metas[i]
                    facts.append(
                        ResearchFact(
                            content=content,
                            source=str(meta.get("source", "")),
                            title=str(meta.get("title")) if meta.get("title") else None,
                            relevance_score=float(cast(Any, meta.get("relevance_score")))
                            if meta.get("relevance_score")
                            else None,
                        )
                    )

        return facts
