import pytest

from core import status
from core.request import Request
from core.response import Response
from core.router import Router, route


@pytest.fixture
def router():
    return Router()


@pytest.mark.asyncio
async def test_route_decorator(router):
    @route("/test", method="GET")
    async def handler(request: Request) -> Response:
        return Response(status_code=status.OK)

    assert "/test" in router.routes
    assert "GET" in router.routes["/test"]
    assert router.routes["/test"]["GET"] == handler


@pytest.mark.asyncio
async def test_dispatch(router):
    router.routes["/test"] = {"GET": lambda request: Response(status_code=status.OK)}
    request = Request(method="GET", path="/test", headers={}, body="")
    response = await router.dispatch(request)
    assert response.status_code == status.OK


@pytest.mark.asyncio
async def test_dispatch_method_not_allowed(router):
    router.routes["/test"] = {"POST": lambda request: Response(status_code=status.OK)}
    request = Request(method="GET", path="/test", headers={}, body="")
    response = await router.dispatch(request)
    assert response.status_code == status.METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_dispatch_not_found(router):
    request = Request(method="GET", path="/not_existent", headers={}, body="")
    response = await router.dispatch(request)
    assert response.status_code == status.NOT_FOUND
