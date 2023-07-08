import asyncio
from asyncio import Transport
from unittest.mock import AsyncMock, MagicMock

import pytest
from httptools import HttpRequestParser

from core.application import Application
from core.http_protocol import HttpProtocol
from core.request import Request


@pytest.mark.asyncio
async def test_connection_made() -> None:
    app = MagicMock(spec=Application)
    transport = MagicMock(spec=Transport)

    protocol = HttpProtocol(app)
    protocol.connection_made(transport)

    assert protocol.transport == transport


@pytest.mark.asyncio
async def test_data_received() -> None:
    app = AsyncMock(spec=Application)
    transport = MagicMock(spec=Transport)
    protocol = HttpProtocol(app)
    protocol.connection_made(transport)

    data = b"GET / HTTP/1.1\r\nHost: localhost:8000\r\n\r\n"
    protocol.data_received(data)

    while not app.handle_request.called:
        await asyncio.sleep(0.1)

    assert transport.write.call_count == 1
    assert transport.close.call_count == 1
    app.handle_request.assert_called_once()


@pytest.mark.asyncio
async def test_handle_request() -> None:
    app = AsyncMock(spec=Application)
    transport = MagicMock(spec=Transport)
    protocol = HttpProtocol(app)
    protocol.connection_made(transport)

    request = Request()
    request.parser = HttpRequestParser(request)
    request.parser.feed_data(b"GET / HTTP/1.1\r\nHost: localhost:8000\r\n\r\n")

    await protocol.handle_request(request)

    assert transport.write.call_count == 1
    assert transport.close.call_count == 1
    app.handle_request.assert_called_with(request)
