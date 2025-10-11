import logging
import time

from openai import AsyncOpenAI

from src.exceptions import LLMError
from src.message import Message


class LLMClient:
    """Client for interacting with LLM API."""

    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    async def get_response(self, messages: list[Message]) -> str:
        """Get response from LLM API for given messages."""
        start_time = time.time()

        try:
            messages_dict = [msg.to_dict() for msg in messages]

            logging.info(f"LLM request: model={self.model}, context_size={len(messages_dict)}")

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages_dict,  # type: ignore[arg-type]
            )

            duration = time.time() - start_time
            logging.info(f"LLM response: duration={duration:.1f}s, status=success")

            content = response.choices[0].message.content
            if content is None:
                raise LLMError("LLM returned empty response")

            return content

        except LLMError:
            raise
        except Exception as e:
            duration = time.time() - start_time
            logging.error(f"LLM API error: {e!s}")
            raise LLMError(f"Failed to get LLM response: {e!s}") from e
