from agentkit.services.llm import create_llm
from langchain_openai import ChatOpenAI


def test_create_llm_openai() -> None:
    llm = create_llm(model="gpt-4o", openai_api_key="test-key")
    assert isinstance(llm, ChatOpenAI)
    assert llm.model_name == "gpt-4o"
    assert llm.openai_api_key.get_secret_value() == "test-key"


def test_create_llm_default() -> None:
    # Should use settings default
    llm = create_llm()
    assert isinstance(llm, ChatOpenAI)
