from core.request import Request
from core.response import Response
from core.router import route


@route("/", method="GET")
async def hello(request: Request) -> Response:
    return Response(body="Hello, world!")


@route("/another", method="GET")
async def another_route(request: Request) -> Response:
    return Response(body="This is another route!")
