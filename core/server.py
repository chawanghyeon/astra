import asyncio
import logging
from core.http_protocol import HttpProtocol
from core.websocket_protocol import WebSocketProtocol
import uvloop
from settings import DEBUG
import signal


class Server:
    def __init__(self, app):
        self.app = app
        self.http_server = None
        self.ws_server = None

        if DEBUG:
            logging.basicConfig(
                level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
            )
        else:
            logging.disable(logging.NOTSET)

    async def run(self, host, port):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = asyncio.get_event_loop()

        for sig in ("SIGINT", "SIGTERM"):
            loop.add_signal_handler(getattr(signal, sig), lambda: asyncio.create_task(self.stop()))

        try:
            self.http_server = await loop.create_server(lambda: HttpProtocol(self.app), host, port)
            self.ws_server = await loop.create_server(
                lambda: WebSocketProtocol(self.app), host, port + 1
            )

            logging.info(f"HTTP Server is running on http://{host}:{port}")
            logging.info(f"WebSocket Server is running on ws://{host}:{port + 1}")

            await asyncio.gather(self.http_server.serve_forever(), self.ws_server.serve_forever())
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")

    async def stop(self):
        logging.info("Shutting down servers...")
        if self.http_server:
            self.http_server.close()
            await self.http_server.wait_closed()
        if self.ws_server:
            self.ws_server.close()
            await self.ws_server.wait_closed()
        logging.info("Servers have been stopped.")

    def is_running(self):
        return self.http_server is not None and self.ws_server is not None
