import gzip

import pytest

from core.request import Request
from core.response import Response
from middlewares.gzip import GzipMiddleware


@pytest.mark.asyncio
async def test_gzip_middleware() -> None:
    middleware = GzipMiddleware()

    test_request = Request()
    test_request.headers["Accept-Encoding"] = "gzip"

    test_response = Response()
    test_response.body = "test body"

    processed_response = await middleware.process_response(test_request, test_response)

    assert processed_response.headers["Content-Encoding"] == "gzip"
    assert processed_response.headers["Vary"] == "Accept-Encoding"
    assert gzip.decompress(processed_response.body) == b"test body"
