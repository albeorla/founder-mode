import os
from unittest.mock import patch

from agentkit.services.llm import create_llm
from langchain_openai import ChatOpenAI
from pydantic import SecretStr


def test_create_llm_openai() -> None:
    llm = create_llm(model="gpt-4o", openai_api_key="test-key")
    assert isinstance(llm, ChatOpenAI)
    assert llm.model_name == "gpt-4o"
    assert isinstance(llm.openai_api_key, SecretStr)
    assert llm.openai_api_key.get_secret_value() == "test-key"


def test_create_llm_default() -> None:
    # Should use settings default
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        llm = create_llm()
        assert isinstance(llm, ChatOpenAI)
