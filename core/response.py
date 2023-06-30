from core import Status


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
        self._headers = self.DEFAULT_HEADERS.copy()
        self.headers = headers if headers else {}
        self._body: bytes = body.encode() if body else b""

    @property
    def headers(self) -> dict[str, str]:
        return self._headers

    @headers.setter
    def headers(self, new_headers: dict[str, str]) -> None:
        self._headers.update({key.lower(): val for key, val in new_headers.items()})

    @property
    def body(self) -> bytes:
        return self._body

    @body.setter
    def body(self, new_body: str) -> None:
        self._body = new_body.encode() if new_body is not None else b""

    def build(self) -> bytes:
        status_line = (
            f"HTTP/1.1 {self.status_code} {Status.get_status_reason(self.status_code)}\r\n"
        )
        header_lines = "".join([f"{key}: {value}\r\n" for key, value in self.headers.items()])
        response = f"{status_line}{header_lines}\r\n".encode() + (self.body or b"")
        return response
