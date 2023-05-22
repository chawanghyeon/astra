from typing import Optional, Tuple
from urllib.parse import urlparse
from core.request import Request
from core.response import Response
from core.status_codes import FORBIDDEN
from middlewares.base import BaseMiddleware
from settings import ALLOWED_HOSTS


class TrustedHostMiddleware(BaseMiddleware):
    async def process_request(self, request: Request) -> Tuple[Request, Optional[Response]]:
        host = urlparse(request.url).hostname
        if host not in ALLOWED_HOSTS:
            return request, Response(
                status=FORBIDDEN,
                content="Invalid host",
            )

        return request, None
