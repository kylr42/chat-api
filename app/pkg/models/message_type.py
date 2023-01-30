from pydantic import Field

from app.pkg.models.base import BaseEnum, BaseModel

__all__ = ["MessageType", "CreateMessageTypeCommand", "MessageTypeFields"]


class BaseUserRole(BaseModel):
    """Base model for user."""


class MessageType(BaseEnum):
    TEXT = "text"


class MessageTypeFields:
    id = Field(description="Message type id.", example=1)
    name = Field(description="Message type name.", example=MessageType.TEXT.value)


class CreateMessageTypeCommand(BaseUserRole):
    name: MessageType = MessageTypeFields.name
