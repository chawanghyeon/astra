import asyncio
import socket
import struct
from typing import Tuple


class WebSocketProtocol(asyncio.Protocol):
    def __init__(self, app):
        self.app = app
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        pass
