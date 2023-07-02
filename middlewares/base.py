from abc import ABC

from core.request import Request
from core.response import Response


class BaseMiddleware(ABC):
    async def process_request(self, request: Request) -> tuple[Request, Response | None]:
        """
        Process the incoming request before it reaches the handler.
        Override this method to add custom pre-processing logic.
        """
        return request, None

    async def process_response(self, request: Request, response: Response) -> Response:
        """
        Process the response before it is sent back to the client.
        Override this method to add custom post-processing logic.
        """
        return response
