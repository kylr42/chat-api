from typing import Dict, Union

from dependency_injector.wiring import inject

from app.internal.pkg.models.sockets import SocketRoutes
from app.pkg.jwt import access_security
from app.pkg.logger import logger
from app.pkg.models import exceptions
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
    try:
        access_token = await access_security(bearer=auth)
    except exceptions.jwt.WrongToken:
        raise UnAuthorized

    logger.info(f"{sid}: connected, {access_token}")
    await router.server.emit("join", {"sid": sid})


@router.on(event="disconnect")
async def disconnect(sid: str):
    logger.info(f"{sid}: disconnected")
