from unittest.mock import MagicMock


def test_fixtures_available(mock_settings: MagicMock, mock_llm: MagicMock) -> None:
    assert mock_settings.openai_api_key == "sk-dummy"
    assert isinstance(mock_llm, MagicMock)
