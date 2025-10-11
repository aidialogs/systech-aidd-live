import os
from dataclasses import dataclass

from src.exceptions import ConfigError


@dataclass
class Config:
    """Application configuration loaded from environment variables."""

    bot_token: str
    llm_api_key: str
    llm_base_url: str
    llm_model: str
    system_prompt: str
    max_context_messages: int

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables with validation."""

        # Required fields
        bot_token = os.getenv("BOT_TOKEN")
        llm_api_key = os.getenv("LLM_API_KEY")
        llm_base_url = os.getenv("LLM_BASE_URL")
        llm_model = os.getenv("LLM_MODEL")

        # Validate required fields
        missing = []
        if not bot_token:
            missing.append("BOT_TOKEN")
        if not llm_api_key:
            missing.append("LLM_API_KEY")
        if not llm_base_url:
            missing.append("LLM_BASE_URL")
        if not llm_model:
            missing.append("LLM_MODEL")

        if missing:
            raise ConfigError(f"Missing required environment variables: {', '.join(missing)}")

        # Type narrowing: after validation, we know these are not None
        assert bot_token is not None
        assert llm_api_key is not None
        assert llm_base_url is not None
        assert llm_model is not None

        # Optional fields with defaults
        system_prompt = os.getenv("SYSTEM_PROMPT", "Ты полезный AI-ассистент")
        max_context_messages = int(os.getenv("MAX_CONTEXT_MESSAGES", "20"))

        return cls(
            bot_token=bot_token,
            llm_api_key=llm_api_key,
            llm_base_url=llm_base_url,
            llm_model=llm_model,
            system_prompt=system_prompt,
            max_context_messages=max_context_messages,
        )
