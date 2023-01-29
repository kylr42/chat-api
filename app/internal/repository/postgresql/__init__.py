from dependency_injector import containers, providers

from .refresh_tokens import JWTRefreshTokenRepository
from .user import UserRepository

__all__ = ["Repositories", "JWTRefreshTokenRepository", "UserRepository"]


class Repositories(containers.DeclarativeContainer):
    user_repository = providers.Factory(UserRepository)
    refresh_token_repository = providers.Factory(JWTRefreshTokenRepository)
