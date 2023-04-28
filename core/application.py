from core.router import Router
from core.server import Server


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
        response = await self.router.dispatch(request)
        return response

    def run(self, host, port):
        server = Server(self)
        server.run(host, port)
