import asyncio

from core.websocket import WebSocket


class WebSocketProtocol(asyncio.Protocol):
    def __init__(self, app):
        self.app = app
        self.websocket = None
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        self.websocket = WebSocket(self.transport.get_extra_info("peername"))

    async def data_received(self, data):
        message = await self.websocket.receive()
        asyncio.ensure_future(self.handle_message(message))

    async def handle_message(self, message):
        path = message.path
        await self.app.router.dispatch_websocket(path, self.websocket)

    def connection_lost(self, exc):
        self.transport = None

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
