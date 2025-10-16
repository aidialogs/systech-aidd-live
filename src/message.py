from datetime import datetime


class Message:
    """Represents a chat message with role and content."""

    def __init__(
        self,
        role: str,
        content: str,
        id: int | None = None,  # noqa: A002
        created_at: datetime | None = None,
        content_length: int | None = None,
        is_deleted: bool = False,
    ) -> None:
        self.role = role
        self.content = content
        self.id = id
        self.created_at = created_at
        self.content_length = content_length if content_length is not None else len(content)
        self.is_deleted = is_deleted

    def to_dict(self) -> dict[str, str]:
        """Convert message to dictionary format for API calls."""
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_orm(cls, orm_message: "models.Message") -> "Message":  # type: ignore[name-defined]
        """Create Message from ORM model instance.

        Args:
            orm_message: SQLAlchemy Message model instance

        Returns:
            Message instance
        """
        return cls(
            role=orm_message.role,
            content=orm_message.content,
            id=orm_message.id,
            created_at=orm_message.created_at,
            content_length=orm_message.content_length,
            is_deleted=orm_message.is_deleted,
        )
