from typing import Optional

from pydantic import Field, PositiveInt, SecretStr

from server.pkg.models.base import BaseModel

__all__ = [
    "Room",
    "CreateRoomCommand",
    "ReadRoomByIdQuery",
    "ReadAllRoomsQuery",
]


class RoomFields:
    id = Field(description="Room id.", example=2)
    name = Field(description="Room name.", example="Example Room")
    description = Field(description="Room description.", example="Example Room Description")
    is_archived = Field(description="Room is archived.", example=False, default=False)
    is_favorite = Field(description="Room is favorite.", example=False, default=False)
    access_token = Field(description="User access token.", example="example.access.token")
    user_id = Field(description="User id.", example=2, default=1)


class BaseRoom(BaseModel):
    """Base model for room."""
    ...


class Room(BaseRoom):
    id: PositiveInt = RoomFields.id
    name: str = RoomFields.name
    description: Optional[str] = RoomFields.description
    is_archived: bool = RoomFields.is_archived
    is_favorite: bool = RoomFields.is_favorite


class CreateRoomCommand(BaseModel):
    name: str = RoomFields.name
    description: Optional[str] = RoomFields.description
    access_token: SecretStr = RoomFields.access_token
    user_id: PositiveInt = RoomFields.user_id


class ReadRoomByIdQuery(BaseModel):
    id: PositiveInt = RoomFields.id
    access_token: SecretStr = RoomFields.access_token


class ReadAllRoomsQuery(BaseModel):
    access_token: SecretStr = RoomFields.access_token

