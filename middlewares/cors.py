from core.request import Request
from core.response import Response
from middlewares.base import BaseMiddleware
from settings import ALLOW_ALL_ORIGINS, CORS_ORIGINS


class CORSMiddleware(BaseMiddleware):
    def __init__(self, allow_origins: list[str]):
        super().__init__()
        self.allow_origins = allow_origins if allow_origins is not None else CORS_ORIGINS
        self.allow_all_origins = ALLOW_ALL_ORIGINS

    async def process_request(self, request: Request) -> tuple[Request, Response | None]:
        origin = request.headers.get("Origin", "*")

        if origin in self.allow_origins or self.allow_all_origins:
            request.headers["Access-Control-Allow-Origin"] = origin
            request.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            request.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

            if request.method == "OPTIONS":
                response = Response(status_code=204)
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
                response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
                response.headers["Access-Control-Max-Age"] = "86400"
                return request, response

        return request, None

    async def process_response(self, request: Request, response: Response) -> Response:
        origin = request.headers.get("Origin", "*")

        if origin in self.allow_origins or self.allow_all_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

        return response
