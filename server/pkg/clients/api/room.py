from typing import List, Optional

import pydantic

from server.pkg import models
from server.pkg.clients.api.client import ChatApiClient

__all__ = ["RoomClient"]


class RoomClient:
    __client__: Optional[ChatApiClient] = None

    def __init__(self, chat_api_client: ChatApiClient):
        self.__client__ = chat_api_client

    async def create_room(self, cmd: models.CreateRoomCommand) -> models.Room:
        response = await self.__client__.make_request(
            path="/room/",
            method="POST",
            auth=cmd.access_token.get_secret_value(),
            json=cmd.to_dict(),
        )
        return models.Room.parse_obj(response)

    async def read_room_by_id(self, query: models.ReadRoomByIdQuery) -> models.Room:
        response = await self.__client__.make_request(
            path=f"/room/{query.id}",
            method="GET",
            auth=query.access_token.get_secret_value(),
        )
        return models.Room.parse_obj(response)

    async def read_all_rooms(
        self, query: models.ReadAllRoomsQuery
    ) -> List[models.Room]:
        response = await self.__client__.make_request(
            path="/room/",
            method="GET",
            auth=query.access_token.get_secret_value(),
        )
        return pydantic.parse_obj_as(List[models.Room], response)
