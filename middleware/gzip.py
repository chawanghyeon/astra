import gzip
from core.middleware import Middleware
from core.request import Request
from core.response import Response


class GzipMiddleware(Middleware):
    async def process_response(self, request: Request, response: Response) -> Response:
        accept_encoding = request.headers.get("Accept-Encoding", "")
        if "gzip" in accept_encoding.lower():
            response.body = gzip.compress(response.body)
            response.headers.update({"Content-Encoding": "gzip", "Vary": "Accept-Encoding"})
        return response
