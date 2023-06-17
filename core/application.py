import glob
import importlib

from typing import Any, Callable

from core.request import Request
from core.response import Response
from core.router import Router
from core.server import Server
from core.database import Database
from core.websocket import WebSocket
from utils.singleton import Singleton
import logging

import settings

# TODO: Think about is it necessary to merge Application and Server classes
# TODO: Think about is it necessary to merge Application.handle_dispatch and router.dispatch methods
# TODO: Think about is it necessary to merge Application.handle_websocket and router.websocket_dispatch methods
# TODO: Think about is it necessary to add async http stack


class Application(metaclass=Singleton):
    def __init__(self):
        logging.basicConfig(
            filename="app.log",
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.router = Router()
        self.middlewares = []
        self.database = Database()
        self.server = Server(self)
        self._load_views()
        self._load_middlewares()

    def _load_module(self, module_name):
        return importlib.import_module(module_name)

    def _load_views(self):
        module_names = [
            view.replace("/", ".").replace(".py", "") for view in glob.glob("views/*.py")
        ]
        for module_name in module_names:
            self._load_module(module_name)

    def _load_middlewares(self):
        for middleware_path in settings.MIDDLEWARE:
            module_name, class_name = middleware_path.rsplit(".", 1)
            module = self._load_module(module_name)
            MiddlewareClass = getattr(module, class_name)
            self.add_middleware(MiddlewareClass())

    def add_route(self, path: str, handler: Callable) -> None:
        self.router.add_route(path, handler)

    def add_middleware(self, middleware: Any) -> None:
        self.middlewares.append(middleware)

    async def handle_request(self, request: Request) -> Response:
        try:
            for middleware in self.middlewares:
                request, response = await middleware.process_request(request)
                if response is not None:
                    return response
        except Exception as e:
            # Log the exception here
            logging.error(f"Error while processing request: {e}")
            return Response(status_code=500, body="Internal Server Error")

        try:
            response = await self.router.dispatch(request)
        except Exception as e:
            # Log the exception here
            logging.error(f"Error while dispatching request: {e}")
            return Response(status_code=500, body="Internal Server Error")

        try:
            for middleware in reversed(self.middlewares):
                response = await middleware.process_response(request, response)
        except Exception as e:
            # Log the exception here
            logging.error(f"Error while processing response: {e}")
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
            logging.error(f"Error while handling WebSocket message: {e}")
            await websocket.close(
                code=1001, reason="An error occurred while handling your message."
            )

    async def run(self, host: str, port: int) -> None:
        self.server.start_and_run_forever(host, port)
