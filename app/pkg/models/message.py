from pydantic.fields import Field
from pydantic.types import PositiveInt

from app.pkg.models.message_type import MessageType
from app.pkg.models.base import BaseModel

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

    text = Field(description="Message text", example="Hello world!")
    message_type_name = Field(description="Message message_type", example=MessageType.TEXT.value)


class BaseMessage(BaseModel):
    """Base model for Message."""


class Message(BaseMessage):
    id: PositiveInt = MessageFields.id
    user_id: PositiveInt = MessageFields.user_id
    room_id: PositiveInt = MessageFields.room_id
    text: str = MessageFields.text
    message_type_name: MessageType = MessageFields.message_type_name


# Commands.
class CreateMessageCommand(BaseMessage):
    user_id: PositiveInt = MessageFields.user_id
    room_id: PositiveInt = MessageFields.room_id
    text: str = MessageFields.text


class UpdateMessageCommand(BaseMessage):
    id: PositiveInt = MessageFields.id
    text: str = MessageFields.text


class DeleteMessageCommand(BaseMessage):
    id: PositiveInt = MessageFields.id


# Query
class ReadMessageQuery(BaseMessage):
    id: PositiveInt = MessageFields.id


class ReadAllRoomMessagesQuery(BaseMessage):
    room_id: PositiveInt = MessageFields.room_id
