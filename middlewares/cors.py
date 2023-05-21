from middlewares.base import BaseMiddleware
from core.request import Request
from core.response import Response
from typing import List, Optional, Tuple


class CORS(BaseMiddleware):
    def __init__(self, app, allow_origins: List[str] = None):
        super().__init__(app)
        self.allow_origins = allow_origins if allow_origins is not None else ["*"]

    async def process_request(self, request: Request) -> Tuple[Request, Optional[Response]]:
        origin = request.headers.get("origin")

        # If the request is from an allowed origin, add the CORS headers
        if origin in self.allow_origins or "*" in self.allow_origins:
            request.headers["Access-Control-Allow-Origin"] = origin
            request.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            request.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

            # If the request is a preflight request, respond immediately
            if request.method == "OPTIONS":
                response = Response(status_code=204)
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
                response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
                response.headers["Access-Control-Max-Age"] = "86400"
                return request, response

        return request, None

    async def process_response(self, request: Request, response: Response) -> Response:
        origin = request.headers.get("origin")

        # If the request is from an allowed origin, add the CORS headers to the response
        if origin in self.allow_origins or "*" in self.allow_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

        return response