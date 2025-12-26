from unittest.mock import AsyncMock, MagicMock

import pytest

from agentkit.infra.config import Settings


@pytest.fixture
def mock_settings() -> MagicMock:
    """Fixture that returns a mocked Settings object."""
    settings = MagicMock(spec=Settings)
    settings.openai_api_key = "sk-dummy"
    settings.tavily_api_key = "tv-dummy"
    settings.model_name = "gpt-mock"
    return settings


@pytest.fixture
def mock_llm() -> MagicMock:
    """Fixture that returns a mocked LLM (BaseChatModel)."""
    llm = MagicMock()
    llm.ainvoke = AsyncMock(return_value=MagicMock(content="Mocked response"))
    llm.invoke = MagicMock(return_value=MagicMock(content="Mocked response"))
    return llm


@pytest.fixture
def mock_search() -> MagicMock:
    """Fixture that returns a mocked TavilySearchService."""
    service = MagicMock()
    service.search = MagicMock(return_value=[{"content": "mock result", "url": "http://mock.com"}])
    service.asearch = AsyncMock(return_value=[{"content": "mock result", "url": "http://mock.com"}])
    return service


@pytest.fixture
def mock_vector_store() -> MagicMock:
    """Fixture that returns a mocked VectorStore."""
    store = MagicMock()
    store.add_texts = MagicMock(return_value=True)
    store.query = MagicMock(return_value=[{"content": "mock vector result", "metadata": {}}])
    return store
