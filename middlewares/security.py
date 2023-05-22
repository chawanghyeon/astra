from core.request import Request
from core.response import Response

from middlewares.base import BaseMiddleware


class SecurityMiddleware(BaseMiddleware):
    SECURITY_HEADERS = {
        "X-DNS-Prefetch-Control": "off",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-Powered-By": "none",
        "X-XSS-Protection": "1; mode=block",
    }

    async def process_response(self, request: Request, response: Response) -> Response:
        """
        Process the response before it is sent back to the client.
        Insert HTTP security headers.
        """
        response.headers.update(self.SECURITY_HEADERS)
        return await super().process_response(request, response)
