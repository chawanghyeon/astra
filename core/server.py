import asyncio
import uvloop
import logging
from core.http_protocol import HttpProtocol
from core.websocket_protocol import WebSocketProtocol


class Server:
    def __init__(self, app):
        self.app = app
        self.http_server = None
        self.ws_server = None

    async def run(self, host, port):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = asyncio.get_event_loop()

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
        finally:
            self.stop()

    def stop(self):
        if self.http_server:
            self.http_server.close()
        if self.ws_server:
            self.ws_server.close()
        logging.info("Servers have been stopped.")
