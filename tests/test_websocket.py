import socket
import pytest
from core.websocket import WebSocket
from settings import SERVER_HOST, SERVER_PORT
from threading import Thread
import time
import subprocess


class Server:
    def __init__(self):
        self.server = None

    def start(self):
        self.server = subprocess.Popen(
            ["python", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def stop(self):
        self.server.terminate()
        self.server.wait()

    def is_ready(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((SERVER_HOST, SERVER_PORT)) == 0


@pytest.fixture(scope="session", autouse=True)
def start_server():
    server = Server()

    # Start the server in a separate thread
    thread = Thread(target=server.start)
    thread.start()

    # Wait for the server to start up
    while not server.is_ready():
        time.sleep(0.01)

    yield  # This is where the testing happens

    # After testing, clean up by terminating the server process
    server.stop()
    thread.join()


@pytest.fixture
async def websocket(start_server):
    # This fixture will provide a WebSocket instance for each test
    uri = f"ws://{SERVER_HOST}:{SERVER_PORT}"
    websocket = WebSocket(uri)
    await websocket.connect()
    yield websocket
    # Ensure the websocket is closed after each test
    if not websocket.websocket.closed:
        await websocket.aclose()


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
    await websocket.send(message)
    received_message = await websocket.receive()
    assert received_message == message


@pytest.mark.asyncio
async def test_close(websocket):
    # Test if connection is closed
    await websocket.aclose()
    assert websocket.websocket.closed
