from core import Request, Response
from middlewares import BaseMiddleware


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
        return response
