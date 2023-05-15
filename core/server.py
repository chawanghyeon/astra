import asyncio
import uvloop
from core.httpprotocol import HttpProtocol
from core.websocketprotocol import WebSocketProtocol


class Server:
    def __init__(self, app):
        self.app = app

    async def run(self, host, port):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = asyncio.get_event_loop()
        http_server = await loop.create_server(lambda: HttpProtocol(self.app), host, port)
        ws_server = await loop.create_server(lambda: WebSocketProtocol(self.app), host, port + 1)
        print(f"Server is running on http://{host}:{port}")

        print(f"HTTP Server is running on http://{host}:{port}")
        print(f"WebSocket Server is running on ws://{host}:{port + 1}")

        async with http_server, ws_server:
            await asyncio.gather(http_server.serve_forever(), ws_server.serve_forever())
