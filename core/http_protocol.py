# type: ignore

import asyncio

from httptools import HttpParserError, HttpRequestParser

from core.request import Request


class HttpProtocol(asyncio.Protocol):
    def __init__(self, app):
        self.app = app
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        request = Request()
        request.parser = HttpRequestParser(request)

        try:
            request.parser.feed_data(data)
        except HttpParserError:
            self.transport.close()
            return

        asyncio.ensure_future(self.handle_request(request))

        if not request.parser.should_keep_alive():
            self.transport.close()

    async def handle_request(self, request):
        try:
            response = await self.app.handle_request(request)
            self.transport.write(response.build())
            self.transport.close()
        except Exception as e:
            # Handle or log the error here. For example:
            print(f"Error handling request: {e}")
