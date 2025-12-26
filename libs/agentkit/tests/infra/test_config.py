import os
from unittest.mock import patch

from agentkit.infra.config import Settings, get_settings


def test_settings_load_from_env() -> None:
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "MODEL_NAME": "test-model"}):
        # We need to ensure we get a fresh settings instance for the test

        # if it's a singleton. For now, let's assume we can instantiate it.

        settings = Settings()

        assert settings.openai_api_key == "test-key"

        assert settings.model_name == "test-model"


def test_get_settings_singleton() -> None:
    s1 = get_settings()

    s2 = get_settings()

    assert s1 is s2


def test_settings_overrides() -> None:
    settings = Settings(model_name="overridden")

    assert settings.model_name == "overridden"
