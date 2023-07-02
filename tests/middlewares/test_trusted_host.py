import pytest

from core.request import Request
from core.status import Status
from middlewares.trusted_host import TrustedHostMiddleware
from settings import ALLOWED_HOSTS


def create_request_with_headers(headers: dict[str, str]) -> Request:
    request = Request()
    for key, value in headers.items():
        request.on_header(key.encode(), value.encode())
    return request


@pytest.mark.asyncio
async def test_trusted_host_middleware() -> None:
    middleware = TrustedHostMiddleware()

    allowed_host_request = create_request_with_headers({"host": ALLOWED_HOSTS[0]})
    processed_request, response = await middleware.process_request(allowed_host_request)
    assert response is None

    not_allowed_host_request = create_request_with_headers({"host": "not.allowed.host"})
    processed_request, response = await middleware.process_request(not_allowed_host_request)
    assert response is not None
    assert response.status_code == Status.FORBIDDEN
