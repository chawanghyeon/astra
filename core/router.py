from collections.abc import Callable, Coroutine
from typing import Any

from core import Request, Response, Status, WebSocket
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

            return Response(status_code=Status.METHOD_NOT_ALLOWED)

        return Response(status_code=Status.NOT_FOUND, body="Not found")

    async def dispatch_websocket(self, path: str, websocket: WebSocket) -> None:
        handler = self.websocket_routes.get(path)
        if handler:
            message = await websocket.receive()
            response = await handler(message)
            await websocket.send(response)
        else:
            await websocket.close()


router = Router()


def route(path: str, method: str = "GET") -> Callable[[Any], Any]:
    method = method.upper()

    def decorator(handler: Coroutine[Any, Any, Any]) -> Coroutine[Any, Any, Any]:
        router.routes[path][method] = handler
        return handler

    return decorator


def websocket_route(path: str) -> Callable[[Any], Any]:
    def decorator(handler: Coroutine[Any, Any, Any]) -> Coroutine[Any, Any, Any]:
        router.websocket_routes[path] = handler
        return handler

    return decorator
