import os
import uuid
from typing import Any, cast

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from chromadb.utils import embedding_functions
from langchain_openai import OpenAIEmbeddings

from foundermode.domain.schema import ResearchFact


class ChromaLangChainAdapter(EmbeddingFunction[Documents]):  # type: ignore
    def __init__(self, langchain_embeddings: Any) -> None:
        self._langchain_embeddings = langchain_embeddings

    def __call__(self, input: Documents) -> Embeddings:
        return cast(Embeddings, self._langchain_embeddings.embed_documents(input))


class ChromaManager:
    def __init__(self, persist_directory: str = ".chroma_db", collection_name: str = "founder_mode_memory") -> None:
        self.client = chromadb.PersistentClient(path=persist_directory)

        api_key = os.getenv("OPENAI_API_KEY")
        self.embedding_fn: EmbeddingFunction[Any]
        if api_key:
            langchain_emb = OpenAIEmbeddings(model="text-embedding-3-small")
            self.embedding_fn = ChromaLangChainAdapter(langchain_emb)
        else:
            # Fallback for tests if no key is present
            self.embedding_fn = cast(EmbeddingFunction[Any], embedding_functions.DefaultEmbeddingFunction())

        self.collection = self.client.get_or_create_collection(
            name=collection_name, embedding_function=cast(Any, self.embedding_fn)
        )

    def add_facts(self, facts: list[ResearchFact]) -> bool:
        if not facts:
            return True

        documents = [f.content for f in facts]
        metadatas = [
            cast(
                dict[str, Any],
                {"source": f.source, "title": f.title or "", "relevance_score": f.relevance_score or 0.0},
            )
            for f in facts
        ]
        ids = [str(uuid.uuid4()) for _ in facts]

        try:
            self.collection.add(documents=documents, metadatas=cast(Any, metadatas), ids=ids)
            return True
        except Exception as e:
            print(f"Error adding facts: {e}")
            return False

    def query_similar(self, query: str, k: int = 3) -> list[ResearchFact]:
        results = self.collection.query(query_texts=[query], n_results=k)

        facts = []
        if results["documents"]:
            # results is a dict of lists of lists (batch queries)
            # We queried one text, so we take index 0
            docs = results["documents"][0]
            metas = results["metadatas"][0] if results["metadatas"] else None
            # dists = results['distances'][0] # usage optional

            if docs and metas:  # Verify they are not None
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
