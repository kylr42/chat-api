from typing import Dict

from dependency_injector.wiring import inject

from app.internal.pkg.models.sockets import SocketRoutes

router = SocketRoutes()

__all__ = ["router"]


@router.on(event="chat")
@inject
async def user_invite_to_chat_handler(
    sid: str,
    message: Dict[str, str],
):
    await router.server.emit("chat", {"sid": sid, "message": message})
