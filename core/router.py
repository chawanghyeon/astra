from core.response import Response


class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, handler):
        self.routes[path.encode()] = handler

    async def dispatch(self, request):
        handler = self.routes.get(request.path)
        if handler:
            response = await handler(request)
            return response
        else:
            return Response(status_code=404, body=b"Not found")
