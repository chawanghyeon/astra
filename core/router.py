from collections import defaultdict
from typing import Callable
from core.response import Response
from core.status_codes import METHOD_NOT_ALLOWED, NOT_FOUND
from utils.singleton import Singleton


class Router(metaclass=Singleton):
    def __init__(self):
        self.routes = defaultdict(dict)
        self.websocket_routes = defaultdict(dict)

    async def dispatch(self, request) -> Response:
        path_routes = self.routes.get(request.path)
        if path_routes:
            handler = path_routes.get(request.method)
            if handler:
                return await handler(request)

            return Response(status_code=METHOD_NOT_ALLOWED, body="Method not allowed")

        return Response(status_code=NOT_FOUND, body="Not found")

    async def dispatch_websocket(self, path, websocket) -> None:
        handler = self.websocket_routes.get(path)
        if handler:
            async for message in websocket:
                response = await handler(message)
                await websocket.send(response)
        else:
            await websocket.close(code=1001, reason="No handler found for this path.")


router = Router()


def route(path: str, method: str = "GET") -> Callable:
    method = method.upper()

    def decorator(handler: Callable) -> Callable:
        router.routes[path][method] = handler
        return handler

    return decorator


def websocket_route(path: str) -> Callable:
    def decorator(handler: Callable) -> Callable:
        router.websocket_routes[path] = handler
        return handler

    return decorator
