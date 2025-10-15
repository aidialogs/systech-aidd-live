"""Tests for Config class."""

from pathlib import Path

import pytest

from src.config import Config
from src.exceptions import ConfigError


def test_config_from_env_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test successful Config loading from environment variables."""
    monkeypatch.setenv("BOT_TOKEN", "test_bot_token")
    monkeypatch.setenv("LLM_API_KEY", "test_api_key")
    monkeypatch.setenv("LLM_BASE_URL", "https://test.api.com")
    monkeypatch.setenv("LLM_MODEL", "test-model")
    monkeypatch.setenv("SYSTEM_PROMPT", "Custom prompt")
    monkeypatch.setenv("MAX_CONTEXT_MESSAGES", "30")

    config = Config.from_env()

    assert config.bot_token == "test_bot_token"
    assert config.llm_api_key == "test_api_key"
    assert config.llm_base_url == "https://test.api.com"
    assert config.llm_model == "test-model"
    assert config.system_prompt == "Custom prompt"
    assert config.max_context_messages == 30


def test_config_from_env_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test Config with default values for optional parameters."""
    monkeypatch.setenv("BOT_TOKEN", "test_bot_token")
    monkeypatch.setenv("LLM_API_KEY", "test_api_key")
    monkeypatch.setenv("LLM_BASE_URL", "https://test.api.com")
    monkeypatch.setenv("LLM_MODEL", "test-model")

    config = Config.from_env()

    assert config.system_prompt == "Ты полезный AI-ассистент"
    assert config.max_context_messages == 20


def test_config_missing_bot_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test ConfigError when BOT_TOKEN is missing."""
    monkeypatch.setenv("LLM_API_KEY", "test_api_key")
    monkeypatch.setenv("LLM_BASE_URL", "https://test.api.com")
    monkeypatch.setenv("LLM_MODEL", "test-model")

    with pytest.raises(ConfigError) as exc_info:
        Config.from_env()

    assert "BOT_TOKEN" in str(exc_info.value)


def test_config_missing_multiple_vars() -> None:
    """Test ConfigError lists all missing variables."""
    # No environment variables set

    with pytest.raises(ConfigError) as exc_info:
        Config.from_env()

    error_msg = str(exc_info.value)
    assert "BOT_TOKEN" in error_msg
    assert "LLM_API_KEY" in error_msg
    assert "LLM_BASE_URL" in error_msg
    assert "LLM_MODEL" in error_msg


def test_config_as_dataclass() -> None:
    """Test that Config is a proper dataclass."""
    config = Config(
        bot_token="token",
        llm_api_key="key",
        llm_base_url="url",
        llm_model="model",
        system_prompt="prompt",
        max_context_messages=10,
        api_host="0.0.0.0",
        api_port=8000,
    )

    assert config.bot_token == "token"
    assert config.llm_api_key == "key"
    assert config.llm_base_url == "url"
    assert config.llm_model == "model"
    assert config.system_prompt == "prompt"
    assert config.max_context_messages == 10


def test_config_loads_system_prompt_from_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Test Config loads system prompt from file when SYSTEM_PROMPT_FILE is set."""
    # Create a temporary prompt file
    prompt_file = tmp_path / "test_prompt.txt"
    prompt_file.write_text("Test system prompt from file", encoding="utf-8")

    # Set environment variables
    monkeypatch.setenv("BOT_TOKEN", "test_bot_token")
    monkeypatch.setenv("LLM_API_KEY", "test_api_key")
    monkeypatch.setenv("LLM_BASE_URL", "https://test.api.com")
    monkeypatch.setenv("LLM_MODEL", "test-model")
    monkeypatch.setenv("SYSTEM_PROMPT_FILE", str(prompt_file))

    config = Config.from_env()

    assert config.system_prompt == "Test system prompt from file"


def test_config_fallback_to_env_var_when_file_not_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test Config falls back to SYSTEM_PROMPT env var when file is not set."""
    monkeypatch.setenv("BOT_TOKEN", "test_bot_token")
    monkeypatch.setenv("LLM_API_KEY", "test_api_key")
    monkeypatch.setenv("LLM_BASE_URL", "https://test.api.com")
    monkeypatch.setenv("LLM_MODEL", "test-model")
    monkeypatch.setenv("SYSTEM_PROMPT", "Prompt from env var")
    # SYSTEM_PROMPT_FILE not set

    config = Config.from_env()

    assert config.system_prompt == "Prompt from env var"


def test_config_fallback_when_file_not_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test Config falls back to env var when file does not exist."""
    monkeypatch.setenv("BOT_TOKEN", "test_bot_token")
    monkeypatch.setenv("LLM_API_KEY", "test_api_key")
    monkeypatch.setenv("LLM_BASE_URL", "https://test.api.com")
    monkeypatch.setenv("LLM_MODEL", "test-model")
    monkeypatch.setenv("SYSTEM_PROMPT", "Fallback prompt")
    monkeypatch.setenv("SYSTEM_PROMPT_FILE", "/nonexistent/file.txt")

    config = Config.from_env()

    assert config.system_prompt == "Fallback prompt"
