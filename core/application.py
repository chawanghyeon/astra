from core.request import Request
from core.response import Response
from core.router import Router
from core.middleware import Middleware
from core.server import Server
import asyncio

import importlib
import inspect
import glob


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Application(metaclass=Singleton):
    def __init__(self):
        self.router = Router()
        self.middlewares = []

        views = glob.glob("views/*.py")
        for view in views:
            module_name = view.replace("/", ".").replace(".py", "")
            module = importlib.import_module(module_name)
            for name, func in inspect.getmembers(module, inspect.isfunction):
                if hasattr(func, "_route_path"):
                    self.router.add_route(
                        func._route_path[0], func, func._route_path[1]
                    )

    def add_route(self, path: str, handler: callable) -> None:
        self.router.add_route(path, handler)

    def add_middleware(self, middleware: Middleware) -> None:
        self.middlewares.append(middleware)

    def route(self, path: str, method: str = "GET") -> callable:
        def decorator(handler) -> callable:
            handler._route_path = (path, method)
            return handler

        return decorator

    async def handle_request(self, request: Request) -> Response:
        for middleware in self.middlewares:
            request, response = await middleware.process_request(request)
            if response:
                return response

        response = await self.router.dispatch(request)

        for middleware in reversed(self.middlewares):
            response = await middleware.process_response(request, response)

        return response

    def run(self, host: str, port: int) -> None:
        server = Server(self)
        asyncio.run(server.run(host, port))
