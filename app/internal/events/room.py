from typing import Dict

from dependency_injector.wiring import Provide, inject

from app.internal import services
from app.internal.pkg.models.sockets import SocketRoutes
from app.pkg import models
from app.pkg.logger import logger

router = SocketRoutes()

__all__ = ["router"]


@router.on(event="chat-create")
@inject
async def chat_create_handler(
    sid: str,
    message: Dict[str, str],
    room_service: services.room.RoomService = Provide[services.Services.room_service],
):
    session = await router.__server__.get_session(sid)
    user_id = session.get("user_id")

    logger.info(f"{user_id}[{sid}] created room: {message['room']}")

    room = await room_service.create_room(
        cmd=models.CreateRoomRequest(
            name=message["room"],
            description=message.get("description", ""),
            user_id=user_id,
        ),
    )
    router.__server__.enter_room(sid, room.id)
    await router.__server__.emit(
        "notifications",
        {
            "sid": sid,
            "message": {
                "type": "success",
                "message": f"Room {message['room']} created",
                "room_id": room.id,
            },
        },
        room=room.id,
    )


@router.on(event="chat-join")
@inject
async def chat_join_handler(
    sid: str,
    message: Dict[str, str],
    room_service: services.room.RoomService = Provide[services.Services.room_service],
):
    session = await router.__server__.get_session(sid)
    user_id = session.get("user_id")

    logger.info(f"{user_id}[{sid}] joined room: {message['room_id']}")

    await room_service.add_user_to_room(
        cmd=models.AddUserToRoomCommand(
            user_id=user_id,
            room_id=message["room_id"],
        ),
    )
    router.__server__.enter_room(sid, message["room_id"])
    await router.__server__.emit(
        "notifications",
        {
            "sid": sid,
            "message": {
                "type": "success",
                "message": f"Joined room {message['room_id']}",
            },
        },
        room=message["room_id"],
    )


@router.on(event="chat-leave")
@inject
async def chat_leave_handler(
    sid: str,
    message: Dict[str, str],
    room_service: services.room.RoomService = Provide[services.Services.room_service],
):
    session = await router.server.get_session(sid)
    chat_id = session.get("chat_id")

    logger.info(f"{chat_id}[{sid}] left room: {message['room']}")

    await room_service.delete_user_room_mapping(
        cmd=models.DeleteUserRoomMappingCommand(
            user_id=chat_id,
            room_id=message["room_id"],
        ),
    )
    await router.server.leave_room(sid, message["room"])
    await router.server.emit(
        "notifications",
        {
            "sid": sid,
            "message": {
                "type": "success",
                "message": f"Left room {message['room']}",
            },
        },
        room=message["room"],
    )


@router.on(event="chat-list")
@inject
async def chat_list_handler(
    sid: str,
    room_service: services.room.RoomService = Provide[services.Services.room_service],
):
    session = await router.server.get_session(sid)
    user_id = session.get("user_id")

    logger.info(f"{user_id}[{sid}] requested room list")

    rooms = await room_service.read_all_user_rooms(
        query=models.ReadAllUserRoomsQuery(
            user_id=user_id,
        ),
    )
    await router.server.emit(
        "notifications",
        {
            "sid": sid,
            "message": {
                "type": "success",
                "message": f"Rooms: {[room.name for room in rooms]}",
                "rooms": [room.to_dict() for room in rooms],
            },
        },
        room=sid,
    )
