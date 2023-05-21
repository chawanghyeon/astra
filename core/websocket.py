import websockets


class WebSocket:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)

    async def send(self, message: str):
        await self.websocket.send(message)

    async def receive(self):
        return await self.websocket.recv()

    async def close(self):
        await self.websocket.close()
