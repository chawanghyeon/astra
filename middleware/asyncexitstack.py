import asyncio
from contextlib import AsyncExitStack
from core.request import Request
from core.response import Response
from typing import Callable, Optional, Tuple


class AsyncExitStackMiddleware(BaseMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.exit_stack = AsyncExitStack()

    async def process_request(self, request: Request) -> Tuple[Request, Optional[Response]]:
        # Enter the exit stack context
        await self.exit_stack.enter_async_context(request)

        return await super().process_request(request)

    async def process_response(self, request: Request, response: Response) -> Response:
        # Exit the exit stack context, this will cleanup any resources managed by the exit stack
        await self.exit_stack.aclose()

        return await super().process_response(request, response)
