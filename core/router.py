from core.response import Response


class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, handler, method="GET") -> None:
        method = method.upper()
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method] = handler

    async def dispatch(self, request) -> Response:
        path_routes = self.routes.get(request.path)
        if path_routes:
            handler = path_routes.get(request.method)
            if handler:
                return await handler(request)

        return Response(status_code=404, body="Not found")
