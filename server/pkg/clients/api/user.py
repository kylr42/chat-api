from typing import Optional

from server.pkg import models
from server.pkg.logger import logger

from server.pkg.models.exceptions.api import BadRequest, UnexpectedStatus

from server.pkg.models.exceptions.user import UserNotFound

from server.pkg.clients.api.client import ChatApiClient

__all__ = ["UserClient"]


class UserClient:
    __client__: Optional[ChatApiClient] = None

    def __init__(self, chat_api_client: ChatApiClient):
        self.__client__ = chat_api_client

    async def read_user_profile(self, query: models.ReadUserProfileQuery) -> models.User:
        response = await self.__client__.make_request(
            path="/user/me/",
            method="GET",
            auth=query.access_token.get_secret_value(),
        )
        return models.User.parse_obj(response)



