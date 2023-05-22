from typing import Optional, Tuple
from core.request import Request
from core.response import Response
from core.status_codes import MOVED_PERMANENTLY
from middlewares.base import BaseMiddleware


class HttpsRedirectMiddleware(BaseMiddleware):
    async def process_request(self, request: Request) -> Tuple[Request, Optional[Response]]:
        """
        Process the incoming request before it reaches the handler.
        If the scheme is not HTTPS, return a redirect response.
        """
        # Use HTTP as a default scheme if it's not set
        scheme = request.scheme or "http"

        if scheme.lower() != "https":
            # Construct the HTTPS URL
            https_url = f"https://{request.host}{request.path}"
            if request.query_string:
                https_url += f"?{request.query_string}"

            # Create the redirect response
            response = Response(status=MOVED_PERMANENTLY, headers={"Location": https_url})

            return request, response

        # If the request is already using HTTPS, proceed as normal
        return await super().process_request(request)
