from dependency_injector import containers, providers

from server.pkg.settings import settings

__all__ = [
    "Services",
]


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )
