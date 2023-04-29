from core.application import Application
from core.response import Response

app = Application()


@app.route("/")
async def hello(request):
    return Response(body=b"Hello, world!")


@app.route("/another")
async def another_route(request):
    return Response(body=b"This is another route!")