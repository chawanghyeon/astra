from core.response import Response
from core.router import route


@route("/", method="GET")
async def hello(request) -> Response:
    return Response(body="Hello, world!")


@route("/another", method="GET")
async def another_route(request) -> Response:
    return Response(body="This is another route!")
