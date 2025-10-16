"""SQLAlchemy ORM models for the application."""

from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class User(Base):
    """Telegram user model."""

    __tablename__ = "users"

    # Telegram user_id as primary key
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    messages: Mapped[list["Message"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Message(Base):
    """Chat message model."""

    __tablename__ = "messages"

    # Auto-increment ID
    id: Mapped[int] = mapped_column(primary_key=True)

    # Relations
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    # Message data
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # system/user/assistant
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_length: Mapped[int] = mapped_column(Integer, nullable=False)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="messages")


# Indexes for performance
Index(
    "idx_messages_user_chat",
    Message.user_id,
    Message.chat_id,
    Message.is_deleted,
    Message.created_at,
)
Index("idx_users_active", User.is_deleted, User.created_at)
