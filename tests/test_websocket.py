import pytest
from core.websocket import WebSocket
from settings import SERVER_HOST, SERVER_PORT

import time
import asyncio
from core.application import Application


@pytest.fixture(scope='session')
def session_event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def server_fixture(session_event_loop):
    app = Application()
    session_event_loop.run_until_complete(app.server.run(SERVER_HOST, SERVER_PORT))

    print(f"HTTP Server is running on http://{SERVER_HOST}:{SERVER_PORT}")

    # Give server some time to start
    timeout = time.time() + 5
    while not app.server.is_ready():
        if time.time() > timeout:
            raise TimeoutError("Server is not ready after 5 seconds.")
        time.sleep(0.01)

    yield  # This is where the testing happens

    # Cleanup after testing
    session_event_loop.run_until_complete(app.server.stop())


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
