from typing import Dict, Union

from dependency_injector.wiring import Provide, inject

from server.internal.pkg.models import SocketRoutes
from server.pkg import clients, models
from server.pkg.logger import logger

router = SocketRoutes()

__all__ = ["router"]


@router.on(event="connect")
@inject
async def connect(
    sid: str,
    _: Dict[str, Union[str, int]],
    auth: str,
    user_client: clients.api.UserClient = Provide[clients.ClientContainers.user_client],
):
    logger.info(f"{sid}: connecting...")

    if user := await user_client.read_user_profile(
        query=models.ReadUserProfileQuery(
            access_token=auth,
        ),
    ):
        return await router.__server__.save_session(
            sid=sid,
            session={
                "access_token": auth,
                "user_id": user.id,
                "username": user.username,
            },
        )

    await router.__server__.disconnect(sid=sid)


@router.on(event="disconnect")
async def disconnect(sid: str):
    logger.info(f"{sid}: disconnected")
    await router.__server__.disconnect(sid=sid)
