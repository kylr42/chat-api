from typing import Dict

from dependency_injector.wiring import Provide, inject

from server.internal.pkg.models import SocketRoutes
from server.pkg import clients, models
from server.pkg.logger import logger

router = SocketRoutes()

__all__ = ["router"]


@router.on(event="send-message")
@inject
async def new_message_handler(
    sid: str,
    message: Dict[str, str],
    message_client: clients.api.MessageClient = Provide[
        clients.ClientContainers.message_client
    ],
):
    logger.info(f"{sid} created room: {message['room_id']}")

    session = await router.__server__.get_session(sid)
    user_id = session.get("user_id")

    if message := await message_client.send_message(
        cmd=models.CreateMessageCommand(
            content=message["content"],
            room_id=message["room_id"],
            user_id=user_id,
            access_token=session.get("access_token"),
        ),
    ):
        return await router.__server__.emit(
            "notifications",
            {
                "sid": sid,
                "message": {
                    "type": "success",
                    "message": f"Message [{message.id}] sent",
                },
            },
            room=message.room_id,
            skip_sid=sid,
        )


@router.on(event="read-room-message")
@inject
async def read_room_messages_handler(
    sid: str,
    message: Dict[str, str],
    message_client: clients.api.MessageClient = Provide[
        clients.ClientContainers.message_client
    ],
):
    logger.info(f"{sid} read room: {message['room_id']}")

    session = await router.__server__.get_session(sid)

    messages = await message_client.read_all_messages(
        query=models.ReadAllMessagesQuery(
            room_id=message["room_id"],
            access_token=session.get("access_token"),
            limit=message.get("limit", 100),
            offset=message.get("offset", 0),
            user_id=session.get("user_id", 1),
        ),
    )
    return await router.__server__.emit(
        "read_room_message",
        {
            "sid": sid,
            "message": {
                "messages": [message.to_dict() for message in messages],
                "limit": message.get("limit", 100),
                "offset": message.get("offset", 0),
            },
        },
        skip_sid=sid,
    )
