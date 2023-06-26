from collections import defaultdict

from core import websocket
from core.request import Request
from core.response import Response
from core.status import METHOD_NOT_ALLOWED, NOT_FOUND
from utils.singleton import Singleton


class Router(metaclass=Singleton):
    def __init__(self) -> None:
        self.routes: defaultdict = defaultdict(dict)
        self.websocket_routes: defaultdict = defaultdict(dict)

    async def dispatch(self, request: Request) -> Response:
        path_routes = self.routes.get(request.path)
        if path_routes:
            handler = path_routes.get(request.method)
            if handler:
                return await handler(request)

            return Response(status_code=METHOD_NOT_ALLOWED)

        return Response(status_code=NOT_FOUND, body="Not found")

    async def dispatch_websocket(self, path: str, websocket: websocket) -> None:
        handler = self.websocket_routes.get(path)
        if handler:
            async for message in websocket:
                response = await handler(message)
                await websocket.send(response)
        else:
            await websocket.close()


router = Router()


def route(path: str, method: str = "GET"):
    method = method.upper()

    def decorator(handler):
        router.routes[path][method] = handler
        return handler

    return decorator


def websocket_route(path: str):
    def decorator(handler):
        router.websocket_routes[path] = handler
        return handler

    return decorator
