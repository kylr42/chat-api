from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Security, status

from app.internal.services import Services
from app.internal.services.message import MessageService
from app.pkg import models
from app.pkg.jwt import JwtAuthorizationCredentials, access_security

router = APIRouter(prefix="/message", tags=["Message"])

__all__ = ["router"]


@router.get(
    "/",
    response_model=List[models.Message],
    status_code=status.HTTP_200_OK,
    description="Get all messages",
)
@inject
async def read_all_room_messages(
    query: models.ReadAllRoomMessagesQuery = Depends(),
    message_service: MessageService = Depends(Provide[Services.message_service]),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    query.user_id = credentials.subject.get("user_id")

    return await message_service.read_all_room_messages(
        query=query,
    )


@router.post(
    "/",
    response_model=models.Message,
    status_code=status.HTTP_201_CREATED,
    description="Create message",
)
@inject
async def create_message(
    cmd: models.CreateMessageCommand,
    message_service: MessageService = Depends(Provide[Services.message_service]),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    cmd.user_id = credentials.subject.get("user_id")

    return await message_service.create_message(cmd=cmd)


@router.get(
    "/{message_id:int}",
    response_model=models.Message,
    status_code=status.HTTP_200_OK,
    description="Read specific message",
)
@inject
async def read_message(
    message_id: int = models.MessageFields.id,
    message_service: MessageService = Depends(Provide[Services.message_service]),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await message_service.read_message(
        query=models.ReadMessageQuery(
            id=message_id,
            user_id=credentials.subject.get("user_id"),
        ),
    )


@router.put(
    "/{message_id:int}",
    response_model=models.Message,
    status_code=status.HTTP_200_OK,
    description="Update specific message",
)
@inject
async def update_message(
    cmd: models.UpdateMessageCommand,
    message_service: MessageService = Depends(Provide[Services.message_service]),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    cmd.user_id = credentials.subject.get("user_id")

    return await message_service.update_message(cmd=cmd)


@router.delete(
    "/{message_id:int}",
    response_model=models.Message,
    status_code=status.HTTP_200_OK,
    description="Delete specific message",
)
@inject
async def delete_message(
    message_id: int = models.MessageFields.id,
    message_service: MessageService = Depends(Provide[Services.message_service]),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return await message_service.delete_message(
        cmd=models.DeleteMessageCommand(
            id=message_id,
            user_id=credentials.subject.get("user_id"),
        ),
    )
