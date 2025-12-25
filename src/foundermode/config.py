from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for FounderMode."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    """API key for OpenAI."""

    tavily_api_key: str | None = Field(default=None, alias="TAVILY_API_KEY")
    """API key for Tavily search."""

    model_name: str = Field(default="gpt-4o", alias="MODEL_NAME")
    """LLM model to use."""

    log_level: str = Field(default="INFO", alias="FM_LOG_LEVEL")
    """Logging level."""

    chroma_db_path: str = Field(default=".chroma_db", alias="FM_CHROMA_DB_PATH")
    """Path to ChromaDB storage."""

    @property
    def is_live_mode_capable(self) -> bool:
        """Check if both required API keys are present."""
        return bool(self.openai_api_key and self.tavily_api_key)


# Global settings instance
settings = Settings()
