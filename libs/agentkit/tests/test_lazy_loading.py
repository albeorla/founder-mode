import sys
from unittest.mock import patch


def test_lazy_import_no_playwright() -> None:
    # Simulate playwright not being installed
    with patch.dict(sys.modules, {"playwright": None, "playwright.async_api": None}):
        from agentkit.services.extraction import ExtractionService

        service = ExtractionService()
        # Should not raise ImportError on instantiation
        assert service is not None


def test_lazy_import_no_chromadb() -> None:
    # Simulate chromadb not being installed
    with patch.dict(sys.modules, {"chromadb": None}):
        from agentkit.services.vector_store import ChromaVectorStore

        store = ChromaVectorStore(persist_directory=".tmp")
        # Should not raise ImportError on instantiation
        assert store is not None
