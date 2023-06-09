import asyncio
import logging
import signal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.application import Application

from core.http_protocol import HttpProtocol
from settings import DEBUG


class Server:
    def __init__(self, app: "Application") -> None:
        self.app = app
        self.server: asyncio.Server

        if DEBUG:
            logging.basicConfig(
                level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
            )
        else:
            logging.disable(logging.NOTSET)

    async def run(self, host: str, port: int) -> None:
        loop = asyncio.get_event_loop()
        for sig in ("SIGINT", "SIGTERM"):
            loop.add_signal_handler(getattr(signal, sig), lambda: asyncio.create_task(self.stop()))

        try:
            self.server = await loop.create_server(lambda: HttpProtocol(self.app), host, port)

            logging.info(f"HTTP Server is running on http://{host}:{port}")

            await self.server.serve_forever()
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")

    async def stop(self) -> None:
        logging.info("Shutting down servers...")
        if self.server:
            self.server.close()
            await self.server.wait_closed()

        logging.info("Servers have been stopped.")

    def is_running(self) -> bool:
        return self.server.is_serving() if self.server else False
