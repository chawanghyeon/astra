from core.routing import Router
from core.middleware import Middleware
from core.server import Server
import asyncio


class Application:
    def __init__(self):
        self.router = Router()
        self.middlewares = []

    def add_route(self, path, handler):
        self.router.add_route(path, handler)

    def add_middleware(self, middleware):
        self.middlewares.append(middleware)

    def route(self, path):
        def decorator(handler):
            self.add_route(path, handler)
            return handler

        return decorator

    async def handle_request(self, request):
        for middleware in self.middlewares:
            request, response = await middleware.process_request(request)
            if response:
                return response

        response = await self.router.dispatch(request)

        for middleware in reversed(self.middlewares):
            response = await middleware.process_response(request, response)

        return response

    def run(self, host, port):
        server = Server(self)
        asyncio.run(server.run(host, port))
