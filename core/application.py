# type: ignore

import glob
import importlib
import logging
from collections.abc import Callable
from typing import Any

import settings
from core.database import Database
from core.request import Request
from core.response import Response
from core.router import Router
from core.server import Server
from core.status_codes import INTERNAL_SERVER_ERROR
from core.websocket import WebSocket
from utils.singleton import Singleton


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
        self.router.route(path, handler)

    def add_middleware(self, middleware: Any) -> None:
        self.middlewares.append(middleware)

    async def handle_exception(self, exception, error_msg):
        logging.error(f"{error_msg} {exception}")
        return Response(status_code=INTERNAL_SERVER_ERROR)

    async def process_request(self, request: Request) -> tuple[Request, Response | None]:
        for middleware in self.middlewares:
            request, response = await middleware.process_request(request)
            if response is not None:
                return request, response
        return request, None

    async def process_response(self, request: Request, response: Response) -> Response:
        for middleware in reversed(self.middlewares):
            response = await middleware.process_response(request, response)
        return response

    async def handle_request(self, request: Request) -> Response:
        try:
            request, response = await self.process_request(request)

            if response is not None:
                return response

            response = await self.router.dispatch(request)
            response = await self.process_response(request, response)
        except Exception as e:
            return await self.handle_exception(e, "Error while handling request")

        return response

    async def handle_websocket(self, path: str, websocket: WebSocket) -> None:
        try:
            await self.router.dispatch_websocket(path, websocket)
        except Exception as e:
            # Log the exception here
            logging.error(f"Error while handling WebSocket message: {e}")
            await websocket.close()
