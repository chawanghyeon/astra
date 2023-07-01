import pytest

from core import Request, Response
from middlewares import CORSMiddleware


@pytest.mark.asyncio
async def test_cors_middleware() -> None:
    middleware = CORSMiddleware(allow_origins=["https://example.com"])

    test_request = Request()
    test_request.headers["origin"] = "https://example.com"
    test_request.method = "GET"

    processed_request, none_response = await middleware.process_request(test_request)
    assert processed_request.headers["Access-Control-Allow-Origin"] == "https://example.com"
    assert (
        processed_request.headers["Access-Control-Allow-Methods"]
        == "GET, POST, PUT, DELETE, OPTIONS"
    )
    assert (
        processed_request.headers["Access-Control-Allow-Headers"] == "Content-Type, Authorization"
    )
    assert none_response is None

    test_response = Response()

    processed_response = await middleware.process_response(test_request, test_response)
    assert processed_response.headers["Access-Control-Allow-Origin"] == "https://example.com"
    assert (
        processed_response.headers["Access-Control-Allow-Methods"]
        == "GET, POST, PUT, DELETE, OPTIONS"
    )
    assert (
        processed_response.headers["Access-Control-Allow-Headers"] == "Content-Type, Authorization"
    )
