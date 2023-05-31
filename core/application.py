import asyncio
import uvloop
import glob
import importlib
import inspect

from typing import Any, Callable

from core.request import Request
from core.response import Response
from core.router import Router
from core.server import Server
from core.database import Database
from core.websocket import WebSocket
from utils.singleton import Singleton

import settings


class Application(metaclass=Singleton):
    def __init__(self):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        self.router = Router()
        self.middlewares = []
        self.database = Database()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self._load_views())
        self.loop.create_task(self._load_middlewares())

    async def _load_module(self, module_name):
        return importlib.import_module(module_name)

    async def _load_views(self):
        module_names = [
            view.replace("/", ".").replace(".py", "") for view in glob.glob("views/*.py")
        ]
        for module_name in module_names:
            module = await self._load_module(module_name)
            for name, func in inspect.getmembers(module, inspect.isfunction):
                if hasattr(func, "_route_path"):
                    self.router.add_route(func._route_path[0], func, func._route_path[1])

    async def _load_middlewares(self):
        for middleware_path in settings.MIDDLEWARE:
            module_name, class_name = middleware_path.rsplit(".", 1)
            module = await self._load_module(module_name)
            MiddlewareClass = getattr(module, class_name)
            self.add_middleware(MiddlewareClass(self))

    def add_route(self, path: str, handler: Callable) -> None:
        self.router.add_route(path, handler)

    def add_middleware(self, middleware: Any) -> None:
        self.middlewares.append(middleware)

    def route(self, path: str, method: str = "GET") -> Callable:
        def decorator(handler: Callable) -> Callable:
            handler._route_path = (path, method)
            return handler

        return decorator

    def websocket_route(self, path: str) -> Callable:
        def decorator(handler: Callable) -> Callable:
            self.router.add_websocket_route(path, handler)
            return handler

        return decorator

    async def handle_request(self, request: Request) -> Response:
        try:
            for middleware in self.middlewares:
                request, response = await middleware.process_request(request)
                if response is not None:
                    return response
        except Exception as e:
            # Log the exception here
            print(f"Error while processing request: {e}")
            return Response(status_code=500, body="Internal Server Error")

        try:
            response = await self.router.dispatch(request)
        except Exception as e:
            # Log the exception here
            print(f"Error while dispatching request: {e}")
            return Response(status_code=500, body="Internal Server Error")

        try:
            for middleware in reversed(self.middlewares):
                response = await middleware.process_response(request, response)
        except Exception as e:
            # Log the exception here
            print(f"Error while processing response: {e}")
            return Response(status_code=500, body="Internal Server Error")

        return response

    async def handle_websocket(self, path: str, websocket: WebSocket) -> None:
        try:
            handler = self.router.websocket_dispatch(path)
            if handler is not None:
                async for message in websocket:
                    response = await handler(message)
                    await websocket.send(response)
        except Exception as e:
            # Log the exception here
            print(f"Error while handling WebSocket message: {e}")
            await websocket.close(
                code=1001, reason="An error occurred while handling your message."
            )

    # async def start(self):
    #     await self.database.connect()

    # async def stop(self):
    #     await self.database.disconnect()

    def run(self, host: str, port: int) -> None:
        server = Server(self)
        # asyncio.ensure_future(self.start())
        try:
            server.start_and_run_forever(host, port)
        except KeyboardInterrupt:
            pass
        finally:
            loop = asyncio.get_event_loop()
            # loop.run_until_complete(self.stop())
            loop.close()

    def is_running(self) -> bool:
        return self.loop.is_running()
