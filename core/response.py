class Response:
    DEFAULT_HEADERS = {
        "content-type": "text/plain; charset=utf-8",
        "server": "Astra/1.0",
    }

    def __init__(self, status_code=200, headers=None, body=None):
        self.status_code = status_code
        self.headers = self.DEFAULT_HEADERS.copy()
        if headers is not None:
            self.headers.update({key.lower(): val for key, val in headers.items()})
        self.body = body.encode() if body is not None else b""

    def set_header(self, key, value):
        self.headers[key.lower()] = value

    def set_body(self, body):
        self.body = body.encode() if body is not None else b""

    def build(self):
        status_line = f"HTTP/1.1 {self.status_code} {self._get_status_reason(self.status_code)}\r\n"
        header_lines = "".join(
            [f"{key}: {value}\r\n" for key, value in self.headers.items()]
        )
        response = f"{status_line}{header_lines}\r\n".encode("utf-8") + self.body
        return response

    @staticmethod
    def _get_status_reason(status_code):
        status_reasons = {
            200: "OK",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            404: "Not Found",
            500: "Internal Server Error",
        }
        return status_reasons.get(status_code, "Unknown Status")
