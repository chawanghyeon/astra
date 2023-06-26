import asyncio

import websockets


class WebSocketProtocol(websockets.WebSocketServerProtocol):
    def __init__(self, app, *args, **kwargs):
        self.app = app
        super().__init__(*args, **kwargs)

    async def process_message(self, path, message):
        await self.app.router.dispatch_websocket(path, message)

    async def handler(self):
        try:
            await self.handshake()
        except Exception:
            return

        path = self.path
        try:
            async for message in self:
                asyncio.ensure_future(self.process_message(path, message))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.close()
