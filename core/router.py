from core.response import Response


class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, handler):
        self.routes[path] = handler

    async def dispatch(self, request):
        handler = self.routes.get(request.path)
        if handler:
            response = await handler(request)
            return response
        else:
            return Response("Not found", status_code=404)
