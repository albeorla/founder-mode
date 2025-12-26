"""
Shared pytest fixtures and configuration for the test suite.

This module provides reusable fixtures that eliminate duplication across tests:
- State factories for FounderState
- Mock fixtures for external services (LLM, ChromaManager, TavilySearch)
- Async test support
"""

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from foundermode.domain.schema import InvestmentMemo, ResearchFact
from foundermode.domain.state import FounderState

# =============================================================================
# State Factory Fixtures
# =============================================================================


@pytest.fixture
def base_state() -> FounderState:
    """
    Provides a minimal valid FounderState for testing.

    Use this as a starting point and override specific fields as needed:
        state = base_state
        state["research_question"] = "My custom question"
    """
    return {
        "research_question": "Test Question",
        "research_facts": [],
        "memo_draft": InvestmentMemo(),
        "messages": [],
        "next_step": "init",
        "research_topic": None,
        "search_history": [],
        "critique_history": [],
        "revision_count": 0,
    }


@pytest.fixture
def research_state(base_state: FounderState) -> FounderState:
    """FounderState configured for research phase testing."""
    base_state["next_step"] = "research"
    base_state["research_topic"] = "Test business model"
    return base_state


@pytest.fixture
def sample_facts() -> list[ResearchFact]:
    """Sample research facts for testing."""
    return [
        ResearchFact(content="Fact 1", source="https://example.com/1", relevance_score=0.9),
        ResearchFact(content="Fact 2", source="https://example.com/2", relevance_score=0.8),
    ]


@pytest.fixture
def state_with_facts(research_state: FounderState, sample_facts: list[ResearchFact]) -> FounderState:
    """FounderState with pre-populated research facts."""
    research_state["research_facts"] = sample_facts
    return research_state


# =============================================================================
# Mock Fixtures for External Services
# =============================================================================


@pytest.fixture
def mock_llm() -> MagicMock:
    """
    Provides a mock LLM that returns predictable responses.

    Usage:
        def test_something(mock_llm):
            mock_llm.invoke.return_value.content = "Custom response"
    """
    mock = MagicMock()
    mock.invoke.return_value.content = "Mocked LLM response"
    return mock


@pytest.fixture
def mock_chroma_manager() -> MagicMock:
    """
    Provides a mock ChromaManager for vector store operations.

    Already configured with common method returns.
    """
    mock = MagicMock()
    mock.add_scraped_text.return_value = None
    mock.search.return_value = []
    mock.get_collection_stats.return_value = {"count": 0}
    return mock


@pytest.fixture
def mock_tavily_search() -> MagicMock:
    """
    Provides a mock TavilySearch tool.

    Default returns a single search result. Override as needed:
        mock_tavily_search.invoke.return_value = [...]
    """
    mock = MagicMock()
    mock.invoke.return_value = [
        {
            "url": "https://example.com",
            "title": "Mock Result",
            "content": "Mock search result content",
            "score": 0.9,
        }
    ]
    return mock


@pytest.fixture
def mock_deep_scrape() -> AsyncMock:
    """Provides an async mock for deep_scrape_url tool."""
    mock = AsyncMock()
    mock.return_value = "Scraped content from the page"
    return mock


# =============================================================================
# Patch Context Managers
# =============================================================================


@pytest.fixture
def patch_chroma(mock_chroma_manager: MagicMock) -> Any:
    """
    Context manager that patches ChromaManager across the codebase.

    Usage:
        def test_something(patch_chroma):
            with patch_chroma:
                # ChromaManager is mocked here
                result = my_function()
    """
    return patch(
        "foundermode.graph.nodes.researcher.ChromaManager",
        return_value=mock_chroma_manager,
    )


@pytest.fixture
def patch_tavily(mock_tavily_search: MagicMock) -> Any:
    """
    Context manager that patches TavilySearch.

    Usage:
        def test_something(patch_tavily):
            with patch_tavily:
                # TavilySearch is mocked here
                result = my_function()
    """
    return patch(
        "foundermode.graph.nodes.researcher.TavilySearch",
        return_value=mock_tavily_search,
    )


# =============================================================================
# Async Support
# =============================================================================


@pytest.fixture(scope="session")
def event_loop_policy() -> Any:
    """Use default event loop policy for the session."""
    import asyncio

    return asyncio.DefaultEventLoopPolicy()
