from httptools import HttpRequestParser, HttpParserError
from core.request import Request
import asyncio


class HttpProtocol(asyncio.Protocol):
    def __init__(self, app):
        self.app = app
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        request = Request()
        try:
            request.parser.feed_data(data)
        except HttpParserError:
            self.transport.close()
            return

        if request.parser.should_keep_alive():
            request.parser = HttpRequestParser(request)
        else:
            asyncio.ensure_future(self.handle_request(request))

    async def handle_request(self, request):
        try:
            response = await self.app.handle_request(request)
            self.transport.write(response.build())
        except Exception as e:
            # Handle or log the error here. For example:
            print(f"Error handling request: {e}")

        if not request.parser.should_keep_alive():
            self.transport.close()
