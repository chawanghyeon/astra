import pytest

from core.request import Request
from core.response import Response
from middlewares.cors import CORSMiddleware


@pytest.mark.asyncio
async def test_cors_middleware() -> None:
    middleware = CORSMiddleware(allow_origins=["*"])

    test_request = Request()
    test_request.headers["Origin"] = "http://test.com"

    test_response = Response()
    test_response.body = "test body"

    processed_response = await middleware.process_response(test_request, test_response)

    assert processed_response.headers["Access-Control-Allow-Origin"] == "http://test.com"
    assert (
        processed_response.headers["Access-Control-Allow-Methods"]
        == "GET, POST, PUT, DELETE, OPTIONS"
    )
    assert (
        processed_response.headers["Access-Control-Allow-Headers"] == "Content-Type, Authorization"
    )
