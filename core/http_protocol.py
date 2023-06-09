from asyncio import Protocol, ensure_future
from typing import TYPE_CHECKING, Any

from httptools import HttpParserError, HttpRequestParser

if TYPE_CHECKING:
    from core.application import Application

from core.request import Request


class HttpProtocol(Protocol):
    def __init__(self, app: "Application"):
        self.app = app
        self.transport: Any

    def connection_made(self, transport: Any) -> None:
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        request = Request()
        request.parser = HttpRequestParser(request)

        try:
            request.parser.feed_data(data)
        except HttpParserError:
            self.transport.close()
            return

        ensure_future(self.handle_request(request))

        if not request.parser.should_keep_alive():
            self.transport.close()

    async def handle_request(self, request: Request) -> None:
        response = await self.app.handle_request(request)
        self.transport.write(response.build())  # type: ignore
        self.transport.close()
