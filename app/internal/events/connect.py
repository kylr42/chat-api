from typing import Dict, Union

from dependency_injector.wiring import inject

from app.internal.pkg.models.sockets import SocketRoutes
from app.pkg.models.exceptions.jwt import UnAuthorized

router = SocketRoutes()

__all__ = ["router"]


@router.on(event="connect")
@inject
async def connect(
    sid: str,
    environ: Dict[str, Union[str, int]],
    auth: str,
):
    if not auth:
        await router.server.disconnect(sid=sid)
        raise UnAuthorized

    await router.server.emit("join", {"sid": sid})


@router.on(event="disconnect")
async def disconnect(sid: str):
    print(f"{sid}: disconnected")
