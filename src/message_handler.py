import logging
from src.message import Message


class MessageHandler:
    def __init__(self, llm_client, context_manager, system_prompt):
        self.llm_client = llm_client
        self.context_manager = context_manager
        self.system_prompt = system_prompt
    
    async def handle_message(self, message, user_id, chat_id):
        text = message.text
        
        logging.info(f"Message from user_id={user_id} chat_id={chat_id}: \"{text}\"")
        
        # Обработка команд
        if text == '/start':
            logging.info(f"Command /start from user_id={user_id}")
            return "Привет! Я AI-ассистент. Используй /help для справки."
        
        if text == '/help':
            logging.info(f"Command /help from user_id={user_id}")
            return ("Доступные команды:\n"
                    "/start - Начать диалог\n"
                    "/help - Показать эту справку\n"
                    "/reset - Очистить историю диалога")
        
        if text == '/reset':
            logging.info(f"Command /reset from user_id={user_id}")
            self.context_manager.clear_context(user_id, chat_id)
            return "История диалога очищена. Начнем сначала!"
        
        try:
            # Получить контекст
            context = self.context_manager.get_context(user_id, chat_id)
            
            # Добавить system prompt если контекст пустой
            if not context:
                system_message = Message("system", self.system_prompt)
                self.context_manager.add_message(user_id, chat_id, system_message)
                context = [system_message]
            
            # Добавить user message в контекст
            user_message = Message("user", text)
            self.context_manager.add_message(user_id, chat_id, user_message)
            context.append(user_message)
            
            # Логировать размер контекста
            logging.info(f"Sending to LLM: context_size={len(context)}")
            
            # Получить ответ от LLM
            response = await self.llm_client.get_response(context)
            
            # Добавить assistant message в контекст
            assistant_message = Message("assistant", response)
            self.context_manager.add_message(user_id, chat_id, assistant_message)
            
            return response
        
        except Exception as e:
            logging.error(f"Error handling message: {str(e)}")
            return "Извините, не могу ответить прямо сейчас. Попробуйте чуть позже."


