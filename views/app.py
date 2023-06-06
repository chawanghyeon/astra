from core.response import Response
from core.router import route


@route("/", method="GET")
async def hello(request):
    return Response(body="Hello, world!")


@route("/", method="POST")
async def create_hello(request):
    # Your POST request handling logic here
    pass


@route("/items", method="PUT")
async def update_item(request):
    # Your PUT request handling logic here
    pass


@route("/another", method="GET")
async def another_route(request):
    return Response(body="This is another route!")
