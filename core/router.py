from collections import defaultdict
from core.response import Response
from core.status_codes import METHOD_NOT_ALLOWED, NOT_FOUND


class Router:
    def __init__(self):
        self.routes = defaultdict(dict)
        self.websocket_routes = defaultdict(dict)

    def add_route(self, path, handler, method="GET") -> None:
        method = method.upper()
        self.routes[path][method] = handler

    def add_websocket_route(self, path, handler) -> None:
        self.websocket_routes[path] = handler

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
