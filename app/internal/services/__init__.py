from dependency_injector import containers, providers

from app.internal.repository import Repositories, postgresql
from app.internal.services import auth, user, room
from app.internal.services.auth import AuthService
from app.internal.services.room import RoomService
from app.internal.services.user import UserService
from app.pkg.settings import settings

__all__ = ["Services", "auth", "user", "room"]


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )

    repositories: postgresql.Repositories = providers.Container(
        Repositories.postgres,
    )  # type: ignore

    user_service = providers.Factory(UserService, repositories.user_repository)

    auth_service = providers.Factory(
        AuthService,
        user_service=user_service,
        refresh_token_repository=repositories.refresh_token_repository,
    )

    room_service = providers.Factory(
        RoomService,
        room_repository=repositories.room_repository,
        user_room_mapping_repository=repositories.user_room_mapping_repository,
    )
