import asyncio
import uvloop
from httptools import HttpRequestParser, HttpParserError, parse_url, HttpResponseParser
from core.request import Request
from core.response import Response


class SimpleHttpProtocol(asyncio.Protocol):
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


class Server:
    def __init__(self, app):
        self.app = app

    async def run(self, host, port):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = asyncio.get_event_loop()
        server = await loop.create_server(
            lambda: SimpleHttpProtocol(self.app), host, port
        )
        print(f"Server is running on http://{host}:{port}")

        async with server:
            await server.serve_forever()
