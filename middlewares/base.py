from abc import ABC, abstractmethod
from typing import Callable

from core.request import Request
from core.response import Response


class BaseMiddleware(ABC):
    def __init__(self, app):
        self.app = app

    @abstractmethod
    async def process_request(self, request: Request) -> Request:
        """
        Process the incoming request before it reaches the handler.
        Override this method to add custom pre-processing logic.
        """
        return request

    @abstractmethod
    async def process_response(self, request: Request, response: Response) -> Response:
        """
        Process the response before it is sent back to the client.
        Override this method to add custom post-processing logic.
        """
        return response

    async def __call__(self, handler: Callable, request: Request) -> Response:
        # Process the incoming request
        processed_request = await self.process_request(request)

        # Call the next middleware or handler in the pipeline
        response = await handler(processed_request)

        # Process the outgoing response
        processed_response = await self.process_response(request, response)

        return processed_response
