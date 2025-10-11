import logging
import time
from openai import AsyncOpenAI


class LLMClient:
    def __init__(self, api_key, base_url, model):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    async def get_response(self, messages):
        start_time = time.time()

        try:
            messages_dict = [msg.to_dict() for msg in messages]

            logging.info(f"LLM request: model={self.model}, context_size={len(messages_dict)}")

            response = await self.client.chat.completions.create(
                model=self.model, messages=messages_dict
            )

            duration = time.time() - start_time
            logging.info(f"LLM response: duration={duration:.1f}s, status=success")

            return response.choices[0].message.content

        except Exception as e:
            duration = time.time() - start_time
            logging.error(f"LLM API error: {str(e)}")
            raise
