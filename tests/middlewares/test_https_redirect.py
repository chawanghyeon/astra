import pytest

from core import Request, Status
from middlewares import HttpsRedirectMiddleware


@pytest.mark.asyncio
async def test_https_redirect_middleware() -> None:
    middleware = HttpsRedirectMiddleware()

    test_request = Request()
    test_request.headers["X-Forwarded-Proto"] = "http"
    test_request.headers["host"] = "www.example.com"
    test_request.path = "/test-path"
    test_request.query_string = "param=value"

    processed_request, redirect_response = await middleware.process_request(test_request)

    assert redirect_response is not None
    assert redirect_response.status_code == Status.MOVED_PERMANENTLY
    assert redirect_response.headers["Location"] == "https://www.example.com/test-path?param=value"

    test_request.headers["X-Forwarded-Proto"] = "https"

    processed_request, redirect_response = await middleware.process_request(test_request)

    assert redirect_response is None
