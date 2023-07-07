import pytest
import pytest_asyncio

from core import status
from core.request import Request
from core.response import Response
from core.router import Router, route


async def async_response(request: Request) -> Response:
    return Response(status_code=status.OK)


@pytest_asyncio.fixture(autouse=True)
async def reset_singleton() -> None:
    Router.reset()


@pytest.mark.asyncio
async def test_route_decorator() -> None:
    @route("/test", method="GET")
    async def handler(request: Request) -> Response:
        return Response(status_code=status.OK)

    router = Router()
    assert "/test" in router.routes
    assert router.routes["/test"]["GET"] == handler


@pytest.mark.asyncio
async def test_dispatch() -> None:
    router = Router()
    router.routes["/test"] = {"GET": async_response}
    request = Request()
    request.path = "/test"
    request.method = "GET"
    response = await router.dispatch(request)
    assert response.status_code == status.OK


@pytest.mark.asyncio
async def test_dispatch_method_not_allowed() -> None:
    router = Router()
    router.routes["/test"] = {"POST": async_response}
    request = Request()
    request.path = "/test"
    request.method = "GET"
    response = await router.dispatch(request)
    assert response.status_code == status.METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_dispatch_not_found() -> None:
    router = Router()
    router.routes["/test"] = {"GET": async_response}
    request = Request()
    request.path = "/test/1"
    request.method = "GET"
    response = await router.dispatch(request)
    assert response.status_code == status.NOT_FOUND
