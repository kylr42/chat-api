from pydantic import Field, NonNegativeInt, PositiveInt, SecretStr

from server.pkg.models.base import BaseModel

__all__ = [
    "Message",
    "CreateMessageCommand",
    "ReadMessageByIdQuery",
    "ReadAllMessagesQuery",
]


class MessageFields:
    id = Field(description="Message id.", example=2)
    room_id = Field(description="Room id.", example=2)
    user_id = Field(description="User id.", example=2, default=1)
    content = Field(description="Message content.", example="Hello World!")
    message_type_id = Field(description="Message type id.", example=2, default=1)
    created_at = Field(description="Message created at.", example="2021-01-01 00:00:00")
    access_token = Field(
        description="User access token.",
        example="example.access.token",
    )
    limit = Field(description="Limit of messages.", example=10, default=10)
    offset = Field(description="Offset of messages.", example=0, default=0)


class BaseMessage(BaseModel):
    """Base model for message."""

    ...


class Message(BaseMessage):
    id: PositiveInt = MessageFields.id
    room_id: PositiveInt = MessageFields.room_id
    user_id: PositiveInt = MessageFields.user_id
    content: str = MessageFields.content
    message_type_id: PositiveInt = MessageFields.message_type_id


class CreateMessageCommand(BaseModel):
    room_id: PositiveInt = MessageFields.room_id
    user_id: PositiveInt = MessageFields.user_id
    content: str = MessageFields.content
    message_type_id: PositiveInt = MessageFields.message_type_id
    access_token: SecretStr = MessageFields.access_token


class ReadMessageByIdQuery(BaseModel):
    id: PositiveInt = MessageFields.id
    access_token: SecretStr = MessageFields.access_token


class ReadAllMessagesQuery(BaseModel):
    room_id: PositiveInt = MessageFields.room_id
    limit: NonNegativeInt = MessageFields.limit
    offset: NonNegativeInt = MessageFields.offset
    access_token: SecretStr = MessageFields.access_token
    user_id: PositiveInt = MessageFields.user_id
