from httptools import HttpRequestParser, HttpParserError, parse_url, HttpResponseParser
from core.request import Request
from core.response import Response
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

        if request.parser.should_keep_alive():
            request.parser = HttpRequestParser(request)

        if request.parser.should_upgrade() is False:
            asyncio.ensure_future(self.handle_request(request))

    async def handle_request(self, request):
        response = await self.app.handle_request(request)
        self.transport.write(response.build())
        self.transport.close()
