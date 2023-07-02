import gzip

from core.status import Status


class Response:
    DEFAULT_HEADERS = {
        "content-type": "text/plain; charset=utf-8",
        "server": "Astra/1.0",
    }

    def __init__(
        self,
        status_code: int = Status.OK,
        headers: dict[str, str] = {},
        body: str = "",
    ) -> None:
        self.status_code = status_code
        self.headers = headers if headers else self.DEFAULT_HEADERS
        self.body = body

    def build(self) -> bytes:
        status_line = (
            f"HTTP/1.1 {self.status_code} {Status.get_status_reason(self.status_code)}\r\n"
        )
        header_lines = "".join([f"{key}: {value}\r\n" for key, value in self.headers.items()])
        body = self.body.encode() if isinstance(self.body, str) else self.body
        if self.headers.get("Content-Encoding") == "gzip":
            body = gzip.compress(body)
        response = f"{status_line}{header_lines}\r\n".encode() + (body or b"")
        return response
