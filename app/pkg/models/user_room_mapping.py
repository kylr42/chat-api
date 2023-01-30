from pydantic.fields import Field
from pydantic.types import PositiveInt

from app.pkg.models.base import BaseModel

__all__ = [
    "UserRoomMapping",
    "UserRoomMappingFields",
    "CreateUserRoomMappingCommand",
    "ReadUserRoomMappingByIdQuery",
    "ReadUserRoomMappingByRoomIdQuery",
    "ReadUserRoomMappingByUserIdQuery",
    "UpdateUserRoomMappingCommand",
    "UpdateUserRoomMappingStatusCommand",
    "AddUserToRoomCommand",
    "DeleteUserRoomMappingCommand",
]


class UserRoomMappingFields:
    id = Field(description="Room id.", example=2)
    is_archived = Field(description="Room is archived.", example=True, default=False)
    is_favorite = Field(description="Room is favorite.", example=True, default=False)
    user_id = Field(description="User id.", example=2)
    room_id = Field(description="Room id.", example=2)


class BaseUserRoomMapping(BaseModel):
    """Base model for UserRoomMapping."""


class UserRoomMapping(BaseUserRoomMapping):
    id: PositiveInt = UserRoomMappingFields.id
    is_archived: bool = UserRoomMappingFields.is_archived
    is_favorite: bool = UserRoomMappingFields.is_favorite
    user_id: PositiveInt = UserRoomMappingFields.user_id
    room_id: PositiveInt = UserRoomMappingFields.room_id


# Commands.
class CreateUserRoomMappingCommand(BaseUserRoomMapping):
    user_id: PositiveInt = UserRoomMappingFields.user_id
    room_id: PositiveInt = UserRoomMappingFields.room_id


class UpdateUserRoomMappingCommand(BaseUserRoomMapping):
    id: PositiveInt = UserRoomMappingFields.id
    user_id: PositiveInt = UserRoomMappingFields.user_id
    room_id: PositiveInt = UserRoomMappingFields.room_id


class UpdateUserRoomMappingStatusCommand(BaseUserRoomMapping):
    id: PositiveInt = UserRoomMappingFields.id
    is_archived: bool = UserRoomMappingFields.is_archived
    is_favorite: bool = UserRoomMappingFields.is_favorite


class DeleteUserRoomMappingCommand(BaseUserRoomMapping):
    id: PositiveInt = UserRoomMappingFields.id


class AddUserToRoomCommand(BaseUserRoomMapping):
    user_id: PositiveInt = UserRoomMappingFields.user_id
    room_id: PositiveInt = UserRoomMappingFields.room_id


# Query
class ReadUserRoomMappingByIdQuery(BaseUserRoomMapping):
    id: PositiveInt = UserRoomMappingFields.id


class ReadUserRoomMappingByRoomIdQuery(BaseUserRoomMapping):
    room_id: PositiveInt = UserRoomMappingFields.room_id


class ReadUserRoomMappingByUserIdQuery(BaseUserRoomMapping):
    user_id: PositiveInt = UserRoomMappingFields.user_id
