from typing import Any

from core import status
from core.request import Request
from core.response import Response
from utils.singleton import Singleton


class Router(metaclass=Singleton):
    def __init__(self) -> None:
        self.routes: dict[str, Any] = {}
        self.websocket_routes: dict[str, Any] = {}

    async def dispatch(self, request: Request) -> Response:
        path_routes = self.routes.get(request.path)
        if path_routes:
            handler = path_routes.get(request.method)
            if handler:
                return await handler(request)

            return Response(status_code=status.METHOD_NOT_ALLOWED)

        return Response(status_code=status.NOT_FOUND)

    @classmethod
    def reset(cls) -> None:
        instance = cls()
        instance.routes = {}
        instance.websocket_routes = {}


router = Router()


def route(path: str, method: str = "GET") -> Any:
    method = method.upper()

    def decorator(handler: Any) -> Any:
        if path not in router.routes:
            router.routes[path] = {}
        router.routes[path][method] = handler
        return handler

    return decorator
