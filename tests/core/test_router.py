import pytest

from core import Request, Response, Router, Status, route


@pytest.fixture
def router():
    return Router()


@pytest.mark.asyncio
async def test_route_decorator(router):
    @route("/test", method="GET")
    async def handler(request: Request) -> Response:
        return Response(status_code=Status.OK)

    assert "/test" in router.routes
    assert "GET" in router.routes["/test"]
    assert router.routes["/test"]["GET"] == handler


@pytest.mark.asyncio
async def test_dispatch(router):
    router.routes["/test"] = {"GET": lambda request: Response(status_code=Status.OK)}
    request = Request(method="GET", path="/test", headers={}, body="")
    response = await router.dispatch(request)
    assert response.status_code == Status.OK


@pytest.mark.asyncio
async def test_dispatch_method_not_allowed(router):
    router.routes["/test"] = {"POST": lambda request: Response(status_code=Status.OK)}
    request = Request(method="GET", path="/test", headers={}, body="")
    response = await router.dispatch(request)
    assert response.status_code == Status.METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_dispatch_not_found(router):
    request = Request(method="GET", path="/not_existent", headers={}, body="")
    response = await router.dispatch(request)
    assert response.status_code == Status.NOT_FOUND
