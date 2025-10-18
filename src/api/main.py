"""FastAPI application for statistics and chat API."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from enum import Enum
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.admin_chat_handler import AdminChatHandler
from src.chat_service import ChatService
from src.config import Config
from src.context_manager import ContextManager
from src.database import get_session_factory
from src.exceptions import LLMError
from src.llm_client import LLMClient
from src.mock_stats_collector import MockStatCollector
from src.query_executor import QueryExecutionError, QueryExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class Period(str, Enum):
    """Time period for statistics."""

    SEVEN_DAYS = "7d"
    THIRTY_DAYS = "30d"


class ChatMode(str, Enum):
    """Chat mode."""

    NORMAL = "normal"
    ADMIN = "admin"


# Pydantic models for chat API
class SendMessageRequest(BaseModel):
    """Request model for sending chat message."""

    session_id: str
    message: str
    mode: ChatMode


class ChatResponse(BaseModel):
    """Response model for chat message."""

    message: str
    sql_query: str | None = None
    session_id: str


# Global services
chat_service: ChatService | None = None
session_factory_global = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for FastAPI app."""
    global chat_service, session_factory_global

    # Load configuration
    config = Config.from_env()

    # Initialize database
    session_factory_global = get_session_factory(config.database_url, echo=config.database_echo)

    # Initialize LLM client
    llm_client = LLMClient(config.llm_api_key, config.llm_base_url, config.llm_model)

    # Initialize context manager
    context_manager = ContextManager(
        session_maker=session_factory_global,
        max_context_messages=config.max_context_messages,
    )

    # Initialize chat service
    chat_service = ChatService(llm_client, context_manager, config.system_prompt)

    logging.info("Chat services initialized")

    yield

    # Cleanup
    chat_service = None
    session_factory_global = None
    logging.info("Chat services shut down")


# Create FastAPI application
app = FastAPI(
    title="Systech AIDD API",
    description="API для получения статистики по диалогам и чата с AI-ассистентом",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize statistics collector
stats_collector = MockStatCollector()


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint with API information."""
    return {
        "message": "Systech AIDD Stats API",
        "version": "1.0.0",
        "docs": "/docs",
        "stats_endpoint": "/api/stats",
    }


@app.get("/api/stats")
async def get_stats(
    period: Period = Query(Period.SEVEN_DAYS, description="Период статистики"),
) -> dict[str, Any]:
    """Получить статистику за указанный период.

    Args:
        period: Период для статистики (7d или 30d)

    Returns:
        Статистика с метриками и временным рядом

    Examples:
        - GET /api/stats?period=7d  - статистика за последние 7 дней
        - GET /api/stats?period=30d - статистика за последние 30 дней
    """
    period_days = 7 if period == Period.SEVEN_DAYS else 30
    return await stats_collector.get_stats(period_days)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/api/chat/message")
async def send_chat_message(request: SendMessageRequest) -> ChatResponse:
    """Send message to chat and get response.

    Args:
        request: Chat message request with session_id, message, and mode

    Returns:
        Chat response with message and optional SQL query

    Raises:
        HTTPException: If chat service is not initialized or request fails
    """
    if chat_service is None or session_factory_global is None:
        raise HTTPException(status_code=503, detail="Chat service not initialized")

    try:
        if request.mode == ChatMode.NORMAL:
            # Normal mode: simple chat conversation
            response_text = await chat_service.handle_message(request.session_id, request.message)
            return ChatResponse(
                message=response_text,
                sql_query=None,
                session_id=request.session_id,
            )

        if request.mode == ChatMode.ADMIN:
            # Admin mode: text2sql analytics
            # Create a new query executor for this request
            async with session_factory_global() as session:
                query_executor = QueryExecutor(session)
                admin_handler = AdminChatHandler(chat_service.llm_client, query_executor)

                answer, sql_query = await admin_handler.handle_analytics_question(
                    request.message
                )

                return ChatResponse(
                    message=answer,
                    sql_query=sql_query,
                    session_id=request.session_id,
                )

    except LLMError as e:
        logging.error(f"LLM error: {e!s}")
        raise HTTPException(status_code=500, detail="Failed to get LLM response") from e

    except QueryExecutionError as e:
        logging.error(f"Query execution error: {e!s}")
        raise HTTPException(status_code=400, detail=f"Query execution failed: {e!s}") from e

    except Exception as e:
        logging.error(f"Unexpected error: {e!s}")
        raise HTTPException(status_code=500, detail="Internal server error") from e


@app.get("/api/chat/history/{session_id}")
async def get_chat_history(session_id: str) -> list[dict[str, str]]:
    """Get chat history for a session.

    Args:
        session_id: Session identifier

    Returns:
        List of messages in the chat history

    Note:
        This is a placeholder implementation.
        Full implementation would require storing and retrieving messages.
    """
    # TODO: Implement actual history retrieval from database
    # For now, return empty list since messages are stored but not easily retrievable by session
    return []

