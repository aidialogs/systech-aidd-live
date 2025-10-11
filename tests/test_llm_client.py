from unittest.mock import AsyncMock, patch

import pytest
from dotenv import load_dotenv

from src.config import Config
from src.exceptions import LLMError
from src.llm_client import LLMClient
from src.message import Message


@pytest.mark.asyncio
@pytest.mark.integration
async def test_llm_client_response() -> None:
    """Test that LLM client can get a response."""
    load_dotenv()
    config = Config.from_env()

    client = LLMClient(
        api_key=config.llm_api_key, base_url=config.llm_base_url, model=config.llm_model
    )

    messages = [Message("system", "You are a helpful assistant"), Message("user", "Say hello")]

    response = await client.get_response(messages)

    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_llm_client_successful_response() -> None:
    """Test successful LLM response with mock."""
    client = LLMClient(api_key="test", base_url="https://test.com", model="test-model")

    with patch.object(
        client.client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = "Hello! How can I help you?"
        mock_create.return_value = mock_response

        messages = [Message("user", "test")]

        response = await client.get_response(messages)

        assert response == "Hello! How can I help you?"
        mock_create.assert_called_once()


@pytest.mark.asyncio
async def test_llm_client_empty_response() -> None:
    """Test that LLM client raises error when response content is None."""
    client = LLMClient(api_key="test", base_url="https://test.com", model="test-model")

    with patch.object(
        client.client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = None
        mock_create.return_value = mock_response

        messages = [Message("user", "test")]

        with pytest.raises(LLMError, match="LLM returned empty response"):
            await client.get_response(messages)


@pytest.mark.asyncio
async def test_llm_client_api_error() -> None:
    """Test that LLM client handles API errors properly."""
    client = LLMClient(api_key="test", base_url="https://test.com", model="test-model")

    with patch.object(
        client.client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.side_effect = Exception("API connection failed")

        messages = [Message("user", "test")]

        with pytest.raises(LLMError, match="Failed to get LLM response"):
            await client.get_response(messages)
