from core.application import Application
from core.response import Response

app = Application()


@app.route("/")
async def hello(request):
    return Response("Hello, world!")


@app.route("/another")
async def another_route(request):
    return Response("This is another route!")


if __name__ == "__main__":
    app.run(host="localhost", port=8080)
