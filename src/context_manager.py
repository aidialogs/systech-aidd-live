import logging


class ContextManager:
    def __init__(self, max_context_messages):
        self.contexts = {}
        self.max_context_messages = max_context_messages
    
    def add_message(self, user_id, chat_id, message):
        key = (user_id, chat_id)
        
        if key not in self.contexts:
            self.contexts[key] = []
            logging.info(f"New context created for user_id={user_id} chat_id={chat_id}")
        
        self.contexts[key].append(message)
        logging.info(f"Message added to context: user_id={user_id} chat_id={chat_id} role={message.role} context_size={len(self.contexts[key])}")
        
        # Обрезка контекста (сохранить system prompt)
        if len(self.contexts[key]) > self.max_context_messages:
            system_msg = self.contexts[key][0]
            old_size = len(self.contexts[key])
            self.contexts[key] = [system_msg] + self.contexts[key][-(self.max_context_messages - 1):]
            logging.info(f"Context trimmed: user_id={user_id} chat_id={chat_id} old_size={old_size} new_size={len(self.contexts[key])}")
    
    def get_context(self, user_id, chat_id):
        key = (user_id, chat_id)
        return self.contexts.get(key, [])
    
    def clear_context(self, user_id, chat_id):
        key = (user_id, chat_id)
        
        if key in self.contexts:
            del self.contexts[key]
            logging.info(f"Context cleared for user_id={user_id} chat_id={chat_id}")
        else:
            logging.info(f"No context to clear for user_id={user_id} chat_id={chat_id}")



