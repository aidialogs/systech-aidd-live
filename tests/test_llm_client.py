import pytest
from dotenv import load_dotenv

from src.config import Config
from src.llm_client import LLMClient
from src.message import Message


@pytest.mark.asyncio
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
