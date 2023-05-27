import socket
import subprocess
import time
import pytest
from threading import Thread
from core.websocket import WebSocket
from settings import SERVER_HOST, SERVER_PORT


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

    @staticmethod
    def is_server_ready(host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((host, port)) == 0

    def is_ready(self):
        return self.is_server_ready(SERVER_HOST, SERVER_PORT)


@pytest.fixture(scope="session", autouse=True)
def server_fixture():
    server = Server()

    thread = Thread(target=server.start)
    thread.start()

    while not server.is_ready():
        time.sleep(0.01)

    yield

    server.stop()
    thread.join()


@pytest.fixture
async def websocket_fixture(server_fixture):
    uri = f"ws://{SERVER_HOST}:{SERVER_PORT}"
    async with WebSocket(uri) as websocket:
        await websocket.connect()
        yield websocket


@pytest.mark.asyncio
async def test_connect(websocket_fixture):
    assert websocket_fixture.websocket.open
    assert websocket_fixture.websocket.remote_address[0] == SERVER_HOST
    assert websocket_fixture.websocket.remote_address[1] == SERVER_PORT


@pytest.mark.asyncio
async def test_send_receive(websocket_fixture):
    message = "Hello, WebSocket!"
    await websocket_fixture.send(message)
    received_message = await websocket_fixture.receive()
    assert received_message == message


@pytest.mark.asyncio
async def test_close(websocket_fixture):
    await websocket_fixture.aclose()
    assert websocket_fixture.websocket.closed
