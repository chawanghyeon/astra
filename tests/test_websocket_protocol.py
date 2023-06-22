import asyncio
import pytest
import websockets
from core.websocket_protocol import WebSocketProtocol  # replace with the actual import

@pytest.mark.asyncio
async def test_websocket_protocol():
    # Define a mock app with a router that handles websocket messages
    class MockApp:
        class MockRouter:
            async def dispatch_websocket(self, path, message):
                assert path == '/test'
                assert message == 'test message'
        router = MockRouter()

    # Create the protocol
    protocol = WebSocketProtocol(MockApp(), None, None)

    # Run the server in the background
    server = await asyncio.start_server(protocol.handler, 'localhost', 8765)

    # Use the websockets client to connect to the server and send a message
    async with websockets.connect('ws://localhost:8765/test') as websocket:
        await websocket.send('test message')

    # Close the server
    server.close()
    await server.wait_closed()
