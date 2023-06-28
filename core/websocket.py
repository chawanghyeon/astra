from websockets.client import WebSocketClientProtocol, connect


class WebSocket:
    def __init__(self, uri: str) -> None:
        self.uri = uri
        self.websocket: WebSocketClientProtocol

    async def connect(self) -> None:
        async with connect(self.uri) as websocket:
            self.websocket = websocket

    async def send(self, message: str) -> None:
        await self.websocket.send(message)

    async def receive(self) -> str | bytes:
        return await self.websocket.recv()

    async def close(self) -> None:
        await self.websocket.close()
