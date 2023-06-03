from typing import Optional, Tuple
from urllib.parse import urlparse
from core.request import Request
from core.response import Response
from core.status_codes import FORBIDDEN
from middlewares.base import BaseMiddleware
from settings import ALLOWED_HOSTS


class TrustedHostMiddleware(BaseMiddleware):
    async def process_request(self, request: Request) -> Tuple[Request, Optional[Response]]:
        host = request.headers.get("host", "")
        if host not in ALLOWED_HOSTS:
            return request, Response(status_code=FORBIDDEN)

        return request, None
