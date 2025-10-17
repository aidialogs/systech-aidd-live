"""FastAPI application for statistics API."""

from typing import Annotated

from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from src.api.chat_handler import ChatHandler
from src.api.chat_schemas import ChatMessage, ChatRequest, ChatResponse
from src.api.protocols import StatCollectorProtocol
from src.api.schemas import Statistics
from src.repository import MessageRepository

# Global collector instance (will be set in create_app)
_stat_collector: StatCollectorProtocol | None = None
_chat_handler: ChatHandler | None = None


def get_stat_collector() -> StatCollectorProtocol:
    """Dependency injection for StatCollector.

    Returns:
        StatCollector instance

    Raises:
        RuntimeError: If collector is not initialized
    """
    if _stat_collector is None:
        raise RuntimeError("StatCollector not initialized. Call create_app() first.")
    return _stat_collector


def get_chat_handler() -> ChatHandler:
    """Dependency injection for ChatHandler.

    Returns:
        ChatHandler instance

    Raises:
        RuntimeError: If handler is not initialized
    """
    if _chat_handler is None:
        raise RuntimeError("ChatHandler not initialized. Call create_app() first.")
    return _chat_handler


def create_app(
    stat_collector: StatCollectorProtocol, chat_handler: ChatHandler | None = None
) -> FastAPI:
    """Create and configure FastAPI application.

    Args:
        stat_collector: StatCollector implementation (Mock or Real)
        chat_handler: ChatHandler for chat endpoints (optional)

    Returns:
        Configured FastAPI application
    """
    global _stat_collector, _chat_handler
    _stat_collector = stat_collector
    _chat_handler = chat_handler

    app = FastAPI(
        title="Statistics Dashboard API",
        description="API for retrieving message statistics for dashboard and chat",
        version="1.0.0",
    )

    # Configure CORS for frontend development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production: specify allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/v1/statistics", response_model=Statistics)
    async def get_statistics(
        period: Annotated[
            str,
            Query(description="Time period: day|week|month|all", pattern="^(day|week|month|all)$"),
        ] = "month",
        collector: StatCollectorProtocol = Depends(get_stat_collector),  # noqa: B008
    ) -> Statistics:
        """Get dashboard statistics for specified period.

        Args:
            period: Time period (day, week, month, or all)
            collector: StatCollector dependency

        Returns:
            Statistics object with complete dashboard data
        """
        return await collector.get_statistics(period)

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Health check endpoint.

        Returns:
            Status message
        """
        return {"status": "ok"}

    # Chat endpoints (only if chat_handler is provided)
    if chat_handler is not None:

        @app.post("/api/v1/chat/message", response_model=ChatResponse)
        async def send_message(
            request: ChatRequest,
            handler: ChatHandler = Depends(get_chat_handler),  # noqa: B008
        ) -> ChatResponse:
            """Send a chat message and get AI response.

            Args:
                request: Chat request with message and mode
                handler: ChatHandler dependency

            Returns:
                Chat response with assistant message
            """
            return await handler.handle_message(request)

        @app.get("/api/v1/chat/history", response_model=list[ChatMessage])
        async def get_history(
            user_id: Annotated[int, Query(description="User ID")],
            chat_id: Annotated[int, Query(description="Chat ID")],
            limit: Annotated[int, Query(description="Maximum messages to return")] = 50,
            handler: ChatHandler = Depends(get_chat_handler),
        ) -> list[ChatMessage]:
            """Get chat history for user and chat.

            Args:
                user_id: User ID
                chat_id: Chat ID
                limit: Maximum number of messages

            Returns:
                List of chat messages
            """
            async with handler.session_maker() as session:
                repo = MessageRepository(session)
                messages = await repo.get_messages(user_id, chat_id, limit)

                # Convert to ChatMessage format (exclude system messages for UI)
                return [
                    ChatMessage(role=msg.role, content=msg.content)
                    for msg in messages
                    if msg.role != "system"
                ]

    return app
