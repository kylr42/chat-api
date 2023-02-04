"""Server configuration.

Collect or build all requirements for startup. Provide global point to
``Server`` instance.
"""

from server.internal.services import Services
from server.pkg.clients import ClientContainers
from server.pkg.connectors import Connectors
from server.pkg.models.core import Container, Containers

__all__ = ["__containers__"]


__containers__ = Containers(
    pkg_name=__name__,
    containers=[
        Container(container=Services),
        Container(container=Connectors),
        Container(container=ClientContainers),
    ],
)


"""
Containers: Containers needs for register all containers.
For start building you *MUST* call wire_packages.

Examples:
    When you using containers without `AsyncServer`::

        __containers__.wire_packages()

    When you using ``AsyncServer`` server, you *MUST* pass an argument
    application instance::

        from socketio import AsyncServer
        server = AsyncServer()
        __containers__.wire_packages(server=server)
"""
