from httptools import HttpRequestParser, parse_url


class Request:
    def __init__(self):
        self.parser = HttpRequestParser(self)
        self.method = None
        self.version = None
        self.path = None
        self.headers = {}
        self.body = None
        self.query_string = None

    def on_url(self, url: bytes):
        self.path = parse_url(url).path.decode()
        if parse_url(url).query:
            self.query_string = parse_url(url).query.decode()

    def on_header(self, name: bytes, value: bytes):
        self.headers[name.decode().lower()] = value.decode()

    def on_body(self, body: bytes):
        self.body = body.decode()

    def on_message_complete(self):
        self.method = self.parser.get_method().decode()
        self.version = self.parser.get_http_version()

    def get_header(self, name: str):
        return self.headers.get(name.lower())

    def __repr__(self):
        return f"<Request method={self.method} path={self.path} version={self.version} headers={self.headers}>"
