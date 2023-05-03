from core.application import Application
from core.response import Response

app = Application()


@app.route("/", method="GET")
async def hello(request):
    return Response(body="Hello, world!")


@app.route("/", method="POST")
async def create_hello(request):
    # Your POST request handling logic here
    pass


@app.route("/items", method="PUT")
async def update_item(request):
    # Your PUT request handling logic here
    pass


@app.route("/another", method="GET")
async def another_route(request):
    return Response(body="This is another route!")
