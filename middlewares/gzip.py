import gzip

from core.request import Request
from core.response import Response
from middlewares.base import BaseMiddleware


class GzipMiddleware(BaseMiddleware):
    async def process_response(self, request: Request, response: Response) -> Response:
        accept_encoding = request.headers.get("Accept-Encoding", "")
        if "gzip" in accept_encoding.lower():
            if isinstance(response.body, str):
                # Encode text data to bytes
                response.body = response.body.encode()
            elif not isinstance(response.body, bytes):
                # You need to handle non-text data (like JSON) here.
                # The specifics depend on what kind of data you're dealing with.
                raise TypeError(
                    f"Cannot compress response body of type {type(response.body).__name__}"
                )

            response.body = gzip.compress(response.body)
            response.headers.update({"Content-Encoding": "gzip", "Vary": "Accept-Encoding"})
        return response
