import pytest

from core import Request, Response
from middlewares import SecurityMiddleware


@pytest.mark.asyncio
async def test_security_middleware() -> None:
    middleware = SecurityMiddleware()

    test_request = Request()

    test_response = Response()

    processed_response = await middleware.process_response(test_request, test_response)

    for header, value in SecurityMiddleware.SECURITY_HEADERS.items():
        assert processed_response.headers[header] == value
