import pytest
from core.websocket import WebSocket
from settings import SERVER_HOST, SERVER_PORT

from threading import Thread
import time
import asyncio
from core.application import Application


class Server:
    def __init__(self):
        self.app = Application()
        self.loop = asyncio.new_event_loop()  # Create new event loop

    def start(self):
        asyncio.set_event_loop(self.loop)  # Set the new event loop for this thread
        self.loop.run_until_complete(self.app.run(SERVER_HOST, SERVER_PORT))

    def stop(self):
        self.loop.close()

    def is_ready(self):
        return self.app.is_running()


@pytest.fixture(scope="session", autouse=True)
def server_fixture():
    server = Server()

    # Start server in a new thread
    thread = Thread(target=server.start)
    thread.start()

    # Give server some time to start
    timeout = time.time() + 5
    while not server.is_ready():
        if time.time() > timeout:
            raise TimeoutError("Server is not ready after 5 seconds.")
        time.sleep(0.01)

    yield  # This is where the testing happens

    # Cleanup after testing
    server.stop()
    thread.join()


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
