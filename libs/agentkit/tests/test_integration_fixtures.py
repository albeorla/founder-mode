from unittest.mock import MagicMock

pytest_plugins = ["agentkit.testing.fixtures"]


def test_service_with_mock_search(mock_search: MagicMock) -> None:
    # Use the mock_search fixture
    results = mock_search.search("test")
    assert results[0]["content"] == "mock result"
    mock_search.search.assert_called_once()


def test_llm_with_mock(mock_llm: MagicMock) -> None:
    # Use the mock_llm fixture
    resp = mock_llm.invoke("hello")
    assert resp.content == "Mocked response"
    mock_llm.invoke.assert_called_once()
