import pytest

from core import Request, Status
from middlewares import TrustedHostMiddleware
from settings import ALLOWED_HOSTS


@pytest.mark.asyncio
async def test_trusted_host_middleware() -> None:
    # create a test instance of TrustedHostMiddleware
    middleware = TrustedHostMiddleware()

    # create a test instance of Request with an allowed host
    allowed_host_request = Request(
        headers={"host": ALLOWED_HOSTS[0]}
    )  # replace with appropriate arguments

    # call process_request method
    processed_request, response = await middleware.process_request(allowed_host_request)

    # check if request is allowed for allowed host
    assert response is None

    # create a test instance of Request with a not allowed host
    not_allowed_host_request = Request(
        headers={"host": "not.allowed.host"}
    )  # replace with appropriate arguments

    # call process_request method
    processed_request, response = await middleware.process_request(not_allowed_host_request)

    # check if request is not allowed for not allowed host
    assert response.status_code == Status.FORBIDDEN
