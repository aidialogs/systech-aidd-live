"""Chat service for handling web chat conversations."""

import logging

from src.exceptions import LLMError
from src.message import Message
from src.protocols import ContextManagerProtocol, LLMClientProtocol

logger = logging.getLogger(__name__)


class ChatService:
    """Service for handling chat conversations."""

    def __init__(
        self,
        llm_client: LLMClientProtocol,
        context_manager: ContextManagerProtocol,
        system_prompt: str,
    ) -> None:
        """Initialize chat service.

        Args:
            llm_client: LLM client for generating responses
            context_manager: Context manager for message history
            system_prompt: System prompt for chat conversations
        """
        self.llm_client = llm_client
        self.context_manager = context_manager
        self.system_prompt = system_prompt

    async def handle_message(self, session_id: str, message: str) -> str:
        """Handle incoming chat message and return bot response.

        Args:
            session_id: Unique session identifier (used as chat_id)
            message: User's message text

        Returns:
            AI assistant's response

        Raises:
            LLMError: If LLM request fails
        """
        # Convert session_id to chat_id (use negative number to distinguish from Telegram)
        user_id = 0  # Web chat user ID
        chat_id = hash(session_id) % 1000000  # Generate consistent chat_id from session_id

        logger.info(f'Chat message from session={session_id}: "{message}"')

        try:
            # Get context
            context = await self.context_manager.get_context(user_id, chat_id)

            # Add system prompt if context is empty
            if not context:
                system_message = Message("system", self.system_prompt)
                await self.context_manager.add_message(user_id, chat_id, system_message)

            # Add user message to context
            user_message = Message("user", message)
            await self.context_manager.add_message(user_id, chat_id, user_message)

            # Get updated context for LLM
            context = await self.context_manager.get_context(user_id, chat_id)

            logger.info(f"Sending to LLM: context_size={len(context)}")

            # Get response from LLM
            response = await self.llm_client.get_response(context)

            # Add assistant message to context
            assistant_message = Message("assistant", response)
            await self.context_manager.add_message(user_id, chat_id, assistant_message)

            return response

        except LLMError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error handling chat message: {e!s}")
            raise LLMError(f"Failed to handle chat message: {e!s}") from e
