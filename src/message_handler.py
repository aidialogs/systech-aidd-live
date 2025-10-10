import logging
from src.message import Message


class MessageHandler:
    def __init__(self, llm_client, system_prompt):
        self.llm_client = llm_client
        self.system_prompt = system_prompt
    
    async def handle_message(self, message, user_id, chat_id):
        text = message.text
        
        logging.info(f"Message from user_id={user_id} chat_id={chat_id}: \"{text}\"")
        
        try:
            messages = [
                Message("system", self.system_prompt),
                Message("user", text)
            ]
            
            response = await self.llm_client.get_response(messages)
            return response
        
        except Exception as e:
            logging.error(f"Error handling message: {str(e)}")
            return "Извините, не могу ответить прямо сейчас. Попробуйте чуть позже."


