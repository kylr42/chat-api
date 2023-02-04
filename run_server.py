from aiohttp import web

from server import create_app

web.run_app(create_app(), port=5000, host="0.0.0.0")
