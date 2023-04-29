from core.request import Request


class Middleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = await self._get_request(scope, receive)
            # Pre-processing actions can be performed here
            response = await self.app(request)
            # Post-processing actions can be performed here
            await self._send_response(response, send)
        else:
            await self.app(scope, receive, send)

    async def _get_request(self, scope, receive):
        request = Request(scope, receive)
        return request

    async def _send_response(self, response, send):
        await send(response.build())
