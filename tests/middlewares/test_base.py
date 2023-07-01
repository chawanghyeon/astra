import pytest

from core import Request, Response
from middlewares import BaseMiddleware


@pytest.mark.asyncio
async def test_base_middleware() -> None:
    middleware = BaseMiddleware()

    test_request = Request()
    test_response = Response()

    processed_request, none_response = await middleware.process_request(test_request)
    assert processed_request == test_request
    assert none_response is None

    processed_response = await middleware.process_response(test_request, test_response)
    assert processed_response == test_response
