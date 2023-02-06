from pydantic.fields import Field
from pydantic.types import NonNegativeInt, PositiveInt

from app.pkg.models.base import BaseModel
from app.pkg.models.message_type import MessageType

__all__ = [
    "Message",
    "MessageFields",
    "CreateMessageCommand",
    "ReadMessageQuery",
    "ReadAllRoomMessagesQuery",
    "UpdateMessageCommand",
    "DeleteMessageCommand",
]


class MessageFields:
    id = Field(description="Message id.", example=2)

    author = Field(description="Message author", example="jsiona")
    user_id = Field(description="Message user_id", example=1)

    room = Field(description="Message room", example="42")
    room_id = Field(description="Message room_id", example=1)

    content = Field(description="Message text", example="Hello world!")
    message_type_name = Field(
        description="Message message_type",
        example=MessageType.TEXT.value,
    )
    message_type_id = Field(description="Message message_type_id", example=1, default=1)

    limit = Field(description="Limit of messages", example=10, default=10)
    offset = Field(description="Offset of messages", example=0, default=0)


class BaseMessage(BaseModel):
    """Base model for Message."""


class Message(BaseMessage):
    id: PositiveInt = MessageFields.id
    user_id: PositiveInt = MessageFields.user_id
    room_id: PositiveInt = MessageFields.room_id
    content: str = MessageFields.content
    message_type_name: MessageType = MessageFields.message_type_name


# Commands.
class CreateMessageCommand(BaseMessage):
    user_id: PositiveInt = MessageFields.user_id
    room_id: PositiveInt = MessageFields.room_id
    content: str = MessageFields.content
    message_type_id: PositiveInt = MessageFields.message_type_id


class UpdateMessageCommand(BaseMessage):
    id: PositiveInt = MessageFields.id
    content: str = MessageFields.content


class DeleteMessageCommand(BaseMessage):
    id: PositiveInt = MessageFields.id
    user_id: PositiveInt = MessageFields.user_id


# Query
class ReadMessageQuery(BaseMessage):
    id: PositiveInt = MessageFields.id


class ReadAllRoomMessagesQuery(BaseMessage):
    room_id: PositiveInt = MessageFields.room_id
    limit: NonNegativeInt = MessageFields.limit
    offset: NonNegativeInt = MessageFields.offset
    user_id: PositiveInt = MessageFields.user_id
