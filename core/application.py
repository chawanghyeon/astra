import glob
import importlib
import logging
from types import ModuleType

import settings
from core import Database, Request, Response, Router, Server, Status
from middlewares import BaseMiddleware
from utils import Singleton


class Application(metaclass=Singleton):
    def __init__(self) -> None:
        logging.basicConfig(
            filename="app.log",
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.router = Router()
        self.middlewares: list[BaseMiddleware] = []
        self.database = Database()
        self.server = Server(self)
        self._load_views()
        self._load_middlewares()

    def _load_module(self, module_name: str) -> ModuleType:
        return importlib.import_module(module_name)

    def _load_views(self) -> None:
        module_names = [
            view.replace("/", ".").replace(".py", "") for view in glob.glob("views/*.py")
        ]
        for module_name in module_names:
            self._load_module(module_name)

    def _load_middlewares(self) -> None:
        for middleware_path in settings.MIDDLEWARE:
            module_name, class_name = middleware_path.rsplit(".", 1)
            module = self._load_module(module_name)
            MiddlewareClass = getattr(module, class_name)
            self.add_middleware(MiddlewareClass())

    def add_middleware(self, middleware: BaseMiddleware) -> None:
        self.middlewares.append(middleware)

    async def handle_exception(self, exception: Exception, error_msg: str) -> Response:
        logging.error(f"{error_msg} {exception}")
        return Response(status_code=Status.INTERNAL_SERVER_ERROR)

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
