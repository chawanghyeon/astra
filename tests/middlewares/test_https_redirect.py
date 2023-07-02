import pytest

from core.request import Request
from core.status import Status
from middlewares.https_redirect import HttpsRedirectMiddleware


class RequestForTest(Request):
    def set_header(self, name: str, value: str) -> None:
        self.headers[name.lower()] = value

    def set_path(self, path: str) -> None:
        self.path = path

    def set_query_string(self, query_string: str) -> None:
        self.query_string = query_string


@pytest.mark.asyncio
async def test_https_redirect_middleware() -> None:
    middleware = HttpsRedirectMiddleware()

    test_request = RequestForTest()
    test_request.set_header("X-Forwarded-Proto", "http")
    test_request.set_header("host", "www.example.com")
    test_request.set_path("/test-path")
    test_request.set_query_string("param=value")

    processed_request, redirect_response = await middleware.process_request(test_request)

    assert redirect_response is not None
    assert redirect_response.status_code == Status.MOVED_PERMANENTLY
    assert redirect_response.headers["location"] == "https://www.example.com/test-path?param=value"

    test_request.set_header("X-Forwarded-Proto", "https")

    processed_request, redirect_response = await middleware.process_request(test_request)

    print(redirect_response)
    assert redirect_response is None
