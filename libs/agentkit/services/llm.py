from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from agentkit.infra.config import get_settings


def create_llm(
    model: str | None = None,
    temperature: float = 0,
    openai_api_key: str | None = None,
    **kwargs: Any,
) -> BaseChatModel:
    """
    Factory to create an LLM instance based on model name.
    """
    settings = get_settings()
    model_name = model or settings.model_name
    api_key = openai_api_key or settings.openai_api_key

    if model_name.startswith("gpt-") or "o1-" in model_name:
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=api_key,
            **kwargs,
        )

    # Default to OpenAI for now
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        openai_api_key=api_key,
        **kwargs,
    )
