import logging
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
    api_host: str
    api_port: int

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

        # Try to load system prompt from file first
        system_prompt_file = os.getenv("SYSTEM_PROMPT_FILE")
        system_prompt = None

        if system_prompt_file:
            try:
                with open(system_prompt_file, encoding="utf-8") as f:
                    system_prompt = f.read().strip()
                logging.info(f"System prompt loaded from file: {system_prompt_file}")
            except (OSError, FileNotFoundError) as e:
                logging.warning(f"Failed to load system prompt from file: {e}")

        # Fallback to SYSTEM_PROMPT env var if not loaded from file
        if not system_prompt:
            system_prompt = os.getenv("SYSTEM_PROMPT", "Ты полезный AI-ассистент")
            logging.info("System prompt loaded from environment variable")

        # Optional fields with defaults
        max_context_messages = int(os.getenv("MAX_CONTEXT_MESSAGES", "20"))

        # API server configuration
        api_host = os.getenv("API_HOST", "0.0.0.0")
        api_port = int(os.getenv("API_PORT", "8000"))

        return cls(
            bot_token=bot_token,
            llm_api_key=llm_api_key,
            llm_base_url=llm_base_url,
            llm_model=llm_model,
            system_prompt=system_prompt,
            max_context_messages=max_context_messages,
            api_host=api_host,
            api_port=api_port,
        )
