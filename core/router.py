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
        handler = self.routes.get(request.path + request.method)
        if handler:
            return await handler(request)

        return Response(status_code=status.METHOD_NOT_ALLOWED)


router = Router()


def route(path: str, method: str = "GET") -> Any:
    method = method.upper()

    def decorator(handler: Any) -> Any:
        router.routes[path + method] = handler
        return handler

    return decorator
