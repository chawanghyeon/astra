import asyncio
import uvloop
from aiohttp import web

from core.router import Router
from core.middleware import security_middleware

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Application:
    def __init__(self):
        self.router = Router()

    def route(self, path):
        return self.router.route(path)

    def middleware(self, middleware_func):
        return self.router.middleware(middleware_func)

    def run(self, host="127.0.0.1", port=8080):
        app = web.Application(middlewares=[security_middleware])
        self.router.register_routes(app)

        web.run_app(app, host=host, port=port)
