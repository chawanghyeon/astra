from core.response import Response


class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, handler) -> None:
        self.routes[path] = handler

    async def dispatch(self, request) -> Response:
        handler = self.routes.get(request.path)

        if handler:
            return await handler(request)

        return Response(status_code=404, body="Not found")
