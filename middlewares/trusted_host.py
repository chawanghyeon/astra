from core import status
from core.request import Request
from core.response import Response
from middlewares.base import BaseMiddleware
from settings import ALLOWED_HOSTS


class TrustedHostMiddleware(BaseMiddleware):
    async def process_request(self, request: Request) -> tuple[Request, Response | None]:
        host = request.headers.get("host", "")
        if host not in ALLOWED_HOSTS:
            return request, Response(status_code=status.FORBIDDEN)

        return request, None
