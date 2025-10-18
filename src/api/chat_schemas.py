"""Pydantic schemas for Chat API."""

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Single chat message."""

    role: str = Field(..., description="Message role: user, assistant, or system")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request to send a chat message."""

    message: str = Field(..., description="User message text")
    mode: str = Field(default="normal", description="Chat mode: normal or admin")
    user_id: int = Field(..., description="User ID")
    chat_id: int = Field(..., description="Chat ID")


class ChatResponse(BaseModel):
    """Response from chat API."""

    message: str = Field(..., description="Assistant response message")
    mode: str = Field(..., description="Chat mode used")
    sql_query: str | None = Field(default=None, description="SQL query (admin mode debug)")


