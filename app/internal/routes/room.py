from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Security
from starlette import status

from app.internal.services import Services
from app.internal.services.room import RoomService
from app.pkg import models
from app.pkg.jwt import JwtAuthorizationCredentials, access_security

router = APIRouter(prefix="/room", tags=["Room"])

__all__ = ["router"]


@router.post(
    "/",
    response_model=models.Room,
    status_code=status.HTTP_201_CREATED,
    description="Create room",
)
@inject
async def create_room(
    cmd: models.CreateRoomCommand,
    room_service: RoomService = Depends(Provide[Services.room_service]),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    cmd.user_id = credentials.subject.get("user_id")

    return await room_service.create_room(cmd=cmd)


@router.get(
    "/",
    response_model=List[models.Room],
    status_code=status.HTTP_200_OK,
    description="Get all rooms",
)
@inject
async def read_all_user_rooms(
    room_service: RoomService = Depends(Provide[Services.room_service]),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    user_id = credentials.subject.get("user_id")

    return await room_service.read_all_user_rooms(
        query=models.ReadAllUserRoomsQuery(user_id=user_id),
    )


@router.get(
    "/{room_id:int}",
    response_model=models.Room,
    status_code=status.HTTP_200_OK,
    description="Read specific room",
)
@inject
async def read_room(
    room_id: int = models.RoomFields.id,
    room_service: RoomService = Depends(Provide[Services.room_service]),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    user_id = credentials.subject.get("user_id")

    return await room_service.read_specific_room_by_id(
        query=models.ReadRoomByIdQuery(room_id=room_id, user_id=user_id),
    )


@router.delete(
    "/{room_id:int}",
    response_model=models.Room,
    status_code=status.HTTP_200_OK,
    description="Delete specific room",
)
@inject
async def delete_room(
    room_id: int = models.RoomFields.id,
    room_service: RoomService = Depends(Provide[Services.room_service]),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    user_id = credentials.subject.get("user_id")

    return await room_service.delete_room(
        cmd=models.DeleteRoomCommand(room_id=room_id, user_id=user_id),
    )


@router.put(
    "/{room_id:int}",
    response_model=models.Room,
    status_code=status.HTTP_200_OK,
    description="Update specific room",
)
@inject
async def update_room(
    cmd: models.UpdateRoomCommand,
    room_id: int = models.RoomFields.id,
    room_service: RoomService = Depends(Provide[Services.room_service]),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    cmd.user_id = credentials.subject.get("user_id")
    cmd.room_id = room_id

    return await room_service.update_room(cmd=cmd)
