import asyncio
from contextlib import AsyncExitStack
from core.request import Request
from core.response import Response
from typing import Callable, Optional, Tuple
from .database import AsyncDBConnection  # Hypothetical database connection class


class AsyncExitStackMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, request: Request) -> Response:
        async with AsyncExitStack() as stack:
            # Suppose we have a database connection to manage
            db_conn = await stack.enter_async_context(AsyncDBConnection())

            # Add the connection to the request, so it's accessible in the handler
            request.db_conn = db_conn

            # Now proceed with request processing and handler invocation
            request, response = await self.process_request(request)

            if not response:
                response = await handler(request)

            response = await self.process_response(request, response)

            # The AsyncExitStack will automatically close the DB connection here
        return response
