from core.middleware import Middleware
from core.request import Request
from core.response import Response
from typing import Callable


class SecurityMiddleware(Middleware):
    async def process_response(self, request: Request, response: Response) -> Response:
        """
        Process the response before it is sent back to the client.
        Adds several security headers to the response.
        """
        # add X-XSS-Protection header
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # add other security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"

        return response
