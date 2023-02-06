from typing import List, Optional

import pydantic

from server.pkg import models
from server.pkg.clients.api.client import ChatApiClient

__all__ = ["MessageClient"]


class MessageClient:
    __client__: Optional[ChatApiClient] = None

    def __init__(self, chat_api_client: ChatApiClient):
        self.__client__ = chat_api_client

    async def send_message(self, cmd: models.CreateMessageCommand) -> models.Message:
        response = await self.__client__.make_request(
            path="/message/",
            method="POST",
            auth=cmd.access_token.get_secret_value(),
        )
        return models.Message.parse_obj(response)

    async def read_message_by_id(
        self, cmd: models.ReadMessageByIdQuery
    ) -> models.Message:
        response = await self.__client__.make_request(
            path=f"/message/{cmd.id}/",
            method="GET",
            auth=cmd.access_token.get_secret_value(),
        )
        return models.Message.parse_obj(response)

    async def read_all_messages(
        self, query: models.ReadAllMessagesQuery
    ) -> List[models.Message]:
        response = await self.__client__.make_request(
            path="/message/",
            method="GET",
            auth=query.access_token.get_secret_value(),
            params=query.to_dict(),
        )
        return pydantic.parse_obj_as(List[models.Message], response)
