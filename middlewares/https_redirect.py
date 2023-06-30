from core import Request, Response, Status
from middlewares import BaseMiddleware


class HttpsRedirectMiddleware(BaseMiddleware):
    async def process_request(self, request: Request) -> tuple[Request, Response | None]:
        """
        Process the incoming request before it reaches the handler.
        If the scheme is not HTTPS, return a redirect response.
        """
        scheme = request.headers.get("X-Forwarded-Proto", "").lower()

        if scheme != "https":
            https_url = f"https://{request.headers['host']}{request.path}"
            if request.query_string:
                https_url += f"?{request.query_string}"

            response = Response(
                status_code=Status.MOVED_PERMANENTLY, headers={"Location": https_url}
            )

            return request, response

        return request, None
