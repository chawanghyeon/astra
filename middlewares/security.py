import logging
from core.request import Request
from core.response import Response
from typing import Optional, Tuple

from middlewares.base import BaseMiddleware

logger = logging.getLogger(__name__)


class SecurityMiddleware(BaseMiddleware):
    SECURITY_HEADERS = {
        "X-DNS-Prefetch-Control": "off",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-Powered-By": "none",
        "X-XSS-Protection": "1; mode=block",
    }

    async def process_request(self, request: Request) -> Tuple[Request, Optional[Response]]:
        """
        Process the incoming request before it reaches the handler.
        Here we log the request method and path using the built-in logging module instead of print.
        """
        logger.info(f"Received {request.method} request for {request.path}")
        return await super().process_request(request)

    async def process_response(self, request: Request, response: Response) -> Response:
        """
        Process the response before it is sent back to the client.
        Insert HTTP security headers.
        """
        response.headers.update(self.SECURITY_HEADERS)
        return await super().process_response(request, response)
