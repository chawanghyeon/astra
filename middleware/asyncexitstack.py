from contextlib import AsyncExitStack
from core.request import Request
from core.response import Response
from typing import Callable
from middleware.base import BaseMiddleware


class AsyncExitStackMiddleware(BaseMiddleware):
    async def enter_context(self, request: Request, stack: AsyncExitStack) -> None:
        """
        Enter the async context for this request.
        This is where you should manage your resources.
        """
        db_conn = await stack.enter_async_context(AsyncDBConnection())
        request.db_conn = db_conn

    async def exit_context(self, request: Request, stack: AsyncExitStack) -> None:
        """
        Exit the async context for this request.
        Any cleanup required when the request is done should be done here.
        """
        # Cleanup can be done here if necessary

    async def __call__(self, handler: Callable, request: Request) -> Response:
        async with AsyncExitStack() as stack:
            await self.enter_context(request, stack)

            request, response = await self.process_request(request)

            if not response:
                response = await handler(request)

            response = await self.process_response(request, response)

            await self.exit_context(request, stack)
        return response
