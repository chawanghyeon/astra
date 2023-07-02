import pytest

from core.request import Request
from core.response import Response
from core.status import Status
from middlewares.security import SecurityMiddleware


def create_response_with_status(status_code: int = Status.OK) -> Response:
    response = Response(status_code=status_code)
    return response


@pytest.mark.asyncio
async def test_security_middleware() -> None:
    middleware = SecurityMiddleware()

    test_request = Request()
    test_response = create_response_with_status()

    processed_response = await middleware.process_response(test_request, test_response)

    for header, value in SecurityMiddleware.SECURITY_HEADERS.items():
        assert processed_response.headers[header] == value
