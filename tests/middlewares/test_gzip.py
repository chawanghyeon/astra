import gzip

import pytest

from core import Request, Response
from middlewares import GzipMiddleware


@pytest.mark.asyncio
async def test_gzip_middleware() -> None:
    # create a test instance of GzipMiddleware
    middleware = GzipMiddleware()

    # create a test instance of Request
    test_request = Request()  # replace with appropriate arguments
    test_request.headers["Accept-Encoding"] = "gzip"

    # create a test instance of Response
    test_response = Response()  # replace with appropriate arguments
    test_response.body = "test body"

    # test process_response method
    processed_response = await middleware.process_response(test_request, test_response)

    assert processed_response.headers["Content-Encoding"] == "gzip"
    assert processed_response.headers["Vary"] == "Accept-Encoding"

    # check if the response body has been compressed correctly
    assert gzip.decompress(processed_response.body) == b"test body"

    # create a test instance of Response with non-string, non-bytes body
    test_response.body = 12345  # integer body

    # test process_response method should raise TypeError
    with pytest.raises(TypeError):
        await middleware.process_response(test_request, test_response)
