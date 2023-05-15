from core.request import Request
from core.response import Response
from typing import Callable, Optional, Tuple


class BaseMiddleware:
    def __init__(self, app):
        self.app = app

    async def process_request(self, request: Request) -> Tuple[Request, Optional[Response]]:
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

    async def __call__(self, handler: Callable, request: Request) -> Response:
        # Process the incoming request
        request, response = await self.process_request(request)

        # If a response is already generated in the process_request, return it
        if response:
            return response

        # Call the next middleware or handler in the pipeline
        response = await handler(request)

        # Process the outgoing response
        response = await self.process_response(request, response)

        return response
