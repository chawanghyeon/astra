from typing import Optional, Tuple
from urllib.parse import urlparse
from core.request import Request
from core.response import Response
from core.status_codes import FORBIDDEN
from middlewares.base import BaseMiddleware


class TrustedHostMiddleware(BaseMiddleware):
    def __init__(self, app, trusted_hosts=None):
        super().__init__(app)
        self.trusted_hosts = trusted_hosts or []

    async def process_request(self, request: Request) -> Tuple[Request, Optional[Response]]:
        host = urlparse(request.url).hostname
        if host not in self.trusted_hosts:
            return request, Response(
                status=FORBIDDEN,
                content="Invalid host",
            )

        return await super().process_request(request)
