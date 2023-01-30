from typing import Dict

from dependency_injector.wiring import Provide, inject

from app.internal import services
from app.internal.pkg.models.sockets import SocketRoutes
from app.pkg import models
from app.pkg.logger import logger

router = SocketRoutes()

__all__ = ["router"]


@router.on(event="send-message")
@inject
async def new_message_handler(
    sid: str,
    message: Dict[str, str],
    message_service: services.message.MessageService = Provide[
        services.Services.message_service
    ],
):
    session = await router.__server__.get_session(sid)
    user_id = session.get("user_id")

    logger.info(f"{user_id}[{sid}] created room: {message['room_id']}")

    await router.__server__.emit(
        "new-message",
        {
            "sid": sid,
            "message": {
                "type": "text",
                "message": message.get("content", ""),
                "user_id": user_id,
            },
        },
        room=message["room_id"],
        skip_sid=sid,
    )
    await message_service.create_message(
        cmd=models.CreateMessageCommand(
            text=message.get("content", ""),
            room_id=message["room_id"],
            user_id=user_id,
        ),
    )


@router.on(event="read-message")
@inject
async def read_message_handler(
    sid: str,
    message: Dict[str, str],
    message_service: services.message.MessageService = Provide[
        services.Services.message_service
    ],
):
    session = await router.__server__.get_session(sid)
    user_id = session.get("user_id")

    logger.info(f"{user_id}[{sid}] read message: {message['message_id']}")

    await message_service.read_message(
        query=models.ReadMessageQuery(message_id=message["message_id"])
    )
    await router.__server__.emit(
        "read-message",
        {
            "sid": sid,
            "message": {
                "type": "text",
                "message": message.get("content", ""),
                "user_id": user_id,
            },
        },
        room=message["room_id"],
        skip_sid=sid,
    )


@router.on(event="delete-message")
@inject
async def delete_message_handler(
    sid: str,
    message: Dict[str, str],
    message_service: services.message.MessageService = Provide[
        services.Services.message_service
    ],
):
    session = await router.__server__.get_session(sid)
    user_id = session.get("user_id")

    logger.info(f"{user_id}[{sid}] deleted message: {message['message_id']}")

    await message_service.delete_message(
        query=models.DeleteMessageCommand(message_id=message["message_id"])
    )
    await router.__server__.emit(
        "delete-message",
        {
            "sid": sid,
            "message": {
                "type": "text",
                "message": message.get("content", ""),
                "user_id": user_id,
            },
        },
        room=message["room_id"],
        skip_sid=sid,
    )


@router.on(event="edit-message")
@inject
async def edit_message_handler(
    sid: str,
    message: Dict[str, str],
    message_service: services.message.MessageService = Provide[
        services.Services.message_service
    ],
):
    session = await router.__server__.get_session(sid)
    user_id = session.get("user_id")

    logger.info(f"{user_id}[{sid}] edited message: {message['message_id']}")

    await message_service.update_message(
        cmd=models.UpdateMessageCommand(
            message_id=message["message_id"],
            text=message.get("content", ""),
        )
    )
    await router.__server__.emit(
        "edit-message",
        {
            "sid": sid,
            "message": {
                "type": "text",
                "message": message.get("content", ""),
                "user_id": user_id,
            },
        },
        room=message["room_id"],
        skip_sid=sid,
    )


@router.on(event="get-messages")
@inject
async def get_messages_handler(
    sid: str,
    message: Dict[str, str],
    message_service: services.message.MessageService = Provide[
        services.Services.message_service
    ],
):
    session = await router.__server__.get_session(sid)
    user_id = session.get("user_id")

    logger.info(f"{user_id}[{sid}] get messages: {message['room_id']}")

    messages = await message_service.read_all_room_messages(
        query=models.ReadAllRoomMessagesQuery(
            room_id=message["room_id"],
            limit=message.get("limit", 10),
            offset=message.get("offset", 0),
        )
    )
    await router.__server__.emit(
        "get-messages",
        {
            "sid": sid,
            "messages": messages,
        },
        room=message["room_id"],
        skip_sid=sid,
    )
