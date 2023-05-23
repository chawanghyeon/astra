import pytest
from core.websocket import WebSocket
from settings import SERVER_HOST, SERVER_PORT
import subprocess
import time


@pytest.fixture(scope="session", autouse=True)
def start_server():
    # Start the server as a subprocess
    server = subprocess.Popen(["python", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Give the server a moment to start.
    time.sleep(1)

    yield  # This is where the testing happens

    # After testing, clean up by terminating the server process
    server.terminate()
    server.wait()


@pytest.fixture
async def websocket():
    # This fixture will provide a WebSocket instance for each test
    uri = "ws://{SERVER_HOST}:{SERVER_PORT}"  # Change this to your WebSocket server URI
    websocket = WebSocket(uri)
    await websocket.connect()
    yield websocket
    await websocket.close()


@pytest.mark.asyncio
async def test_connect(websocket):
    # Test if connection is established
    assert websocket.websocket.open
    assert websocket.websocket.remote_address[0] == SERVER_HOST
    assert websocket.websocket.remote_address[1] == SERVER_PORT


@pytest.mark.asyncio
async def test_send_receive(websocket):
    # Test send and receive functionality
    message = "Hello, WebSocket!"
    await websocket.asend(message)
    received_message = await websocket.receive()
    assert received_message == message


@pytest.mark.asyncio
async def test_close(websocket):
    # Test if connection is closed
    await websocket.aclose()
    assert websocket.websocket.closed
