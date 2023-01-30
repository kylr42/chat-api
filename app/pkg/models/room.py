from typing import Optional

from pydantic.fields import Field
from pydantic.types import PositiveInt

from app.pkg.models.base import BaseModel
from app.pkg.models.user import UserFields

__all__ = [
    "Room",
    "RoomFields",
    "CreateRoomCommand",
    "CreateRoomRequest",
    "ReadRoomByIdQuery",
    "ReadAllUserRoomsQuery",
    "UpdateRoomCommand",
    "DeleteRoomCommand",
]


class RoomFields:
    id = Field(description="Room id.", example=2)
    name = Field(description="Room name", example="TestRoom")
    description = Field(description="Room description", example="Room for testing")
    is_archived = Field(description="Room is archived.", example=True, default=False)
    is_favorite = Field(description="Room is favorite.", example=True, default=False)
    user_id = Field(description="User id.", example=2)


class BaseRoom(BaseModel):
    """Base model for Room."""


class Room(BaseRoom):
    id: PositiveInt = RoomFields.id
    name: str = RoomFields.name
    description: Optional[str] = RoomFields.description
    is_archived: bool = RoomFields.is_archived
    is_favorite: bool = RoomFields.is_favorite


# Commands.
class CreateRoomCommand(BaseRoom):
    name: str = RoomFields.name
    description: Optional[str] = RoomFields.description


class CreateRoomRequest(BaseRoom):
    name: str = RoomFields.name
    description: Optional[str] = RoomFields.description
    user_id: PositiveInt = UserFields.id


class UpdateRoomCommand(BaseRoom):
    id: PositiveInt = RoomFields.id
    user_id: PositiveInt = UserFields.id
    name: str = RoomFields.name
    description: Optional[str] = RoomFields.description


class DeleteRoomCommand(BaseRoom):
    id: PositiveInt = RoomFields.id


# Query
class ReadRoomByIdQuery(BaseRoom):
    id: PositiveInt = RoomFields.id
    user_id: PositiveInt = UserFields.id


class ReadAllUserRoomsQuery(BaseRoom):
    user_id: PositiveInt = UserFields.id
