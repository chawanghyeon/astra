from collections.abc import Callable, Coroutine
from typing import Any

from core import Request, Response, Status
from utils import Singleton


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

            return Response(status_code=Status.METHOD_NOT_ALLOWED)

        return Response(status_code=Status.NOT_FOUND, body="Not found")


router = Router()
Handler = Coroutine[Any, Any, Any]


def route(path: str, method: str = "GET") -> Callable[[Handler], Handler]:
    method = method.upper()

    def decorator(handler: Handler) -> Handler:
        router.routes[path][method] = handler
        return handler

    return decorator
