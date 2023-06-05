import pytest
from core.websocket import WebSocket
from settings import SERVER_HOST, SERVER_PORT


# WebSocket URI
uri = f"ws://{SERVER_HOST}:{SERVER_PORT + 1}"


@pytest.mark.asyncio
async def test_websocket_connect():
    # Instantiate WebSocket class
    websocket = WebSocket(uri)

    # Connect to the WebSocket server
    await websocket.connect()

    # Check if connection was successful
    assert websocket.websocket.open

    # Close connection
    await websocket.close()

    # Close event loop
    websocket.websocket.loop.close()


@pytest.mark.asyncio
async def test_websocket_send_receive():
    # Instantiate WebSocket class
    websocket = WebSocket(uri)

    # Connect to the WebSocket server
    await websocket.connect()

    # Send a message
    message = "Hello, WebSocket!"
    await websocket.send(message)

    # Receive a message
    received_message = await websocket.receive()

    # Check if the received message is correct
    assert received_message == message

    # Close connection
    await websocket.close()


@pytest.mark.asyncio
async def test_websocket_close():
    # Instantiate WebSocket class
    websocket = WebSocket(uri)

    # Connect to the WebSocket server
    await websocket.connect()

    # Close connection
    await websocket.close()

    # Check if connection was closed
    assert websocket.websocket.closed
