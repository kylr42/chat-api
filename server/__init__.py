"""Main factory builder of ``FastAPI`` server. from
app.internal.pkg.middlewares.x_auth_token import get_x_token_key.

app = FastAPI(dependencies=[Depends(get_x_token_key)])
if you need x-auth-token auth
"""

from aiohttp import web

from server.configuration import __containers__
from server.configuration.server import SocketServer

__all__ = ["create_app"]


def create_app() -> web:
    server = SocketServer()
    __containers__.wire_packages()
    return server.app
