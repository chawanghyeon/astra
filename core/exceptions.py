from typing import Optional


class HttpException(Exception):
    def __init__(self, status_code: int, message: Optional[str] = None):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.message:
            return f"{self.status_code}: {self.message}"
        else:
            return f"{self.status_code}"


class BadRequest(HttpException):
    def __init__(self, message="Bad Request"):
        super().__init__(400, message)


class NotFound(HttpException):
    def __init__(self, message="Not Found"):
        super().__init__(404, message)


class InternalServerError(HttpException):
    def __init__(self, message="Internal Server Error"):
        super().__init__(500, message)
