import os


class Config:
    def __init__(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        self.llm_api_key = os.getenv('LLM_API_KEY')
        self.llm_base_url = os.getenv('LLM_BASE_URL')
        self.llm_model = os.getenv('LLM_MODEL')
        self.system_prompt = os.getenv('SYSTEM_PROMPT', 'Ты полезный AI-ассистент')
        self.max_context_messages = int(os.getenv('MAX_CONTEXT_MESSAGES', '20'))


