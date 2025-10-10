class MessageHandler:
    def __init__(self):
        pass
    
    async def handle_message(self, message, user_id, chat_id):
        text = message.text
        return f"Вы написали: {text}"


