import gzip

from core import Request, Response
from middlewares import BaseMiddleware


class GzipMiddleware(BaseMiddleware):
    async def process_response(self, request: Request, response: Response) -> Response:
        accept_encoding = request.headers.get("Accept-Encoding", "")
        if "gzip" in accept_encoding.lower():
            if isinstance(response.body, str):
                response.body = response.body.encode()
            elif not isinstance(response.body, bytes):
                raise TypeError(
                    f"Cannot compress response body of type {type(response.body).__name__}"
                )

            response.body = gzip.compress(response.body)
            response.headers.update({"Content-Encoding": "gzip", "Vary": "Accept-Encoding"})
        return response
