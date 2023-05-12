import gzip
from core.middleware import Middleware
from core.request import Request
from core.response import Response
from typing import Callable


class GzipMiddleware(Middleware):
    async def process_response(self, request: Request, response: Response) -> Response:
        """
        Process the response before it is sent back to the client.
        Compress the response body using gzip compression.
        """
        accept_encoding = request.headers.get("Accept-Encoding", "")
        if "gzip" in accept_encoding.lower():
            response.body = gzip.compress(response.body)
            response.headers.update(
                {"Content-Encoding": "gzip", "Vary": "Accept-Encoding"}
            )
        return response
