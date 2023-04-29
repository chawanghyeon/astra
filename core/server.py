import asyncio
import uvloop
from httptools import HttpRequestParser, HttpParserError, parse_url
from core.request import Request
from core.response import Response


class SimpleHttpProtocol(asyncio.Protocol):
    def __init__(self, app):
        self.app = app
        self.parser = HttpRequestParser(self)
        self.transport = None
        self.headers = {}
        self.url = b""
        self.body = b""

    def on_url(self, url: bytes):
        self.url = url

    def on_header(self, name: bytes, value: bytes):
        self.headers[name] = value

    def on_body(self, body: bytes):
        self.body = body

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        try:
            self.parser.feed_data(data)
        except HttpParserError:
            self.transport.close()

        if self.parser.get_method() and self.parser.get_http_version():
            request = Request()
            request.method = self.parser.get_method()
            request.version = self.parser.get_http_version()
            request.path = parse_url(self.url).path
            request.headers = self.headers
            request.body = self.body

            if self.parser.should_keep_alive():
                self.parser = HttpRequestParser(self)

            if self.parser.should_upgrade() is False:
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
