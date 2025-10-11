"""Tests for Message class."""

from src.message import Message


def test_message_creation() -> None:
    """Test that Message can be created with role and content."""
    msg = Message("user", "Hello")
    assert msg.role == "user"
    assert msg.content == "Hello"


def test_message_to_dict() -> None:
    """Test that Message.to_dict() returns correct dictionary."""
    msg = Message("assistant", "Hi there!")
    result = msg.to_dict()
    assert result == {"role": "assistant", "content": "Hi there!"}


def test_message_system_role() -> None:
    """Test Message with system role."""
    msg = Message("system", "You are a helpful assistant")
    assert msg.role == "system"
    assert msg.content == "You are a helpful assistant"
    assert msg.to_dict() == {"role": "system", "content": "You are a helpful assistant"}


def test_message_with_different_content() -> None:
    """Test Message with various content types."""
    messages = [
        Message("user", "Short"),
        Message("assistant", "A longer message with multiple words"),
        Message("user", ""),  # Empty content
    ]

    assert messages[0].content == "Short"
    assert messages[1].content == "A longer message with multiple words"
    assert messages[2].content == ""
