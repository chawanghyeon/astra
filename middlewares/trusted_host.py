from core.request import Request
from core.response import Response
from core.status import FORBIDDEN
from middlewares.base import BaseMiddleware
from settings import ALLOWED_HOSTS


class TrustedHostMiddleware(BaseMiddleware):
    async def process_request(self, request: Request) -> tuple[Request, Response | None]:
        host = request.headers.get("host", "")
        if host not in ALLOWED_HOSTS:
            return request, Response(status_code=FORBIDDEN)

        return request, None
