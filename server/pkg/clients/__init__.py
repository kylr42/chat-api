from dependency_injector import containers, providers

from server.pkg.clients.api import ChatApiClient, MessageClient, RoomClient, UserClient
from server.pkg.settings import settings

__all__ = ["ClientContainers"]


class ClientContainers(containers.DeclarativeContainer):
    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )

    chat_api_client = providers.Singleton(
        ChatApiClient,
        base_url=configuration.CHAT_API_BASE_URL,
    )

    user_client = providers.Singleton(
        UserClient,
        chat_api_client=chat_api_client,
    )
    room_client = providers.Singleton(
        RoomClient,
        chat_api_client=chat_api_client,
    )
    message_client = providers.Singleton(
        MessageClient,
        chat_api_client=chat_api_client,
    )
