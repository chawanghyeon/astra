import asyncio
from aiohttp import web
from core.request import Request
import uvloop


class Server:
    def __init__(self, app):
        self.app = app

    async def handle_request(self, request):
        req = Request(
            request.method, request.path, request.headers, await request.read()
        )
        for middleware in self.app.middlewares:
            await middleware.process_request(req)

        res = await self.app.handle_request(req)

        for middleware in reversed(self.app.middlewares):
            await middleware.process_response(res)

        return web.Response(body=res.body, status=res.status_code, headers=res.headers)

    def run(self, host, port):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        app = web.Application()
        app.router.add_route("*", "/{tail:.*}", self.handle_request)
        web.run_app(app, host=host, port=port)
