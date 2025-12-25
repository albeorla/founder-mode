import os
from unittest.mock import patch

from foundermode.config import Settings


def test_settings_load_from_env() -> None:
    with patch.dict(
        os.environ,
        {
            "OPENAI_API_KEY": "test-openai-key",
            "TAVILY_API_KEY": "test-tavily-key",
            "FM_LOG_LEVEL": "DEBUG",
        },
    ):
        settings = Settings()
        assert settings.openai_api_key == "test-openai-key"
        assert settings.tavily_api_key == "test-tavily-key"
        assert settings.log_level == "DEBUG"


def test_settings_default_values() -> None:
    with patch.dict(
        os.environ,
        {
            "OPENAI_API_KEY": "test-openai-key",
            "TAVILY_API_KEY": "test-tavily-key",
        },
        clear=True,
    ):
        settings = Settings()
        assert settings.log_level == "INFO"
        assert settings.model_name == "gpt-5.2"  # Default


def test_settings_validation_optional_keys() -> None:
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings(_env_file=None)
        assert settings.openai_api_key is None
        assert settings.tavily_api_key is None
        assert settings.is_live_mode_capable is False


def test_settings_mock_mode_fallback() -> None:
    # If we want to allow missing keys for mock mode, we need a flag.
    # But the current spec says we use "Dynamic Fallback" based on presence of keys.
    # So maybe the keys SHOULD be optional in the Pydantic model,
    # and we validate them manually or just use their presence to decide logic.
    pass
