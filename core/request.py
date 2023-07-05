from typing import Any

from httptools import HttpRequestParser, parse_url


class Request:
    def __init__(self) -> None:
        self.parser = HttpRequestParser(self)
        self.method = ""
        self.version = None
        self.path: str = ""
        self.headers: dict[str, str] = {}
        self.body: str | None = None
        self.query_string: str = ""

    def on_url(self, url: bytes) -> None:
        self.path = parse_url(url).path.decode()
        if parse_url(url).query:
            self.query_string = parse_url(url).query.decode()

    def on_header(self, name: bytes, value: bytes) -> None:
        self.headers[name.decode().lower()] = value.decode()

    def on_body(self, body: bytes) -> None:
        self.body = body.decode()

    def on_message_complete(self) -> None:
        self.method = self.parser.get_method().decode()
        self.version = self.parser.get_http_version()

    def get_header(self, name: str) -> Any | None:
        return self.headers.get(name.lower())

    def __repr__(self) -> str:
        return f"<Request method={self.method} path={self.path} version={self.version}"
