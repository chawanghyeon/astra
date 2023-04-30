from httptools import HttpRequestParser, parse_url


class Request:
    def __init__(self):
        self.parser = HttpRequestParser(self)
        self.method = None
        self.version = None
        self.path = None
        self.headers = {}
        self.body = None

    def on_url(self, url: bytes):
        self.path = parse_url(url).path.decode()

    def on_header(self, name: bytes, value: bytes):
        self.headers[name.decode()] = value.decode()

    def on_body(self, body: bytes):
        self.body = body.decode()

    def on_message_complete(self):
        self.method = self.parser.get_method().decode()
        self.version = self.parser.get_http_version()

    def __repr__(self):
        return f"<Request method={self.method} path={self.path} version={self.version} headers={self.headers}>"
