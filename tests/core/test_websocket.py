from unittest.mock import AsyncMock, patch

import pytest

from core.websocket import WebSocket


# TODO: Make sure to run
@pytest.mark.asyncio
async def test_websocket_connect():
    class AsyncContextManagerMock:
        async def __aenter__(self):
            return AsyncMock()

        async def __aexit__(self, exc_type, exc, tb):
            pass

    mock_websocket = AsyncContextManagerMock()
    with patch("websockets.connect", return_value=mock_websocket) as mock_connect:
        ws = WebSocket("ws://test.com")
        await ws.connect()
        mock_connect.assert_called_once_with("ws://test.com")
        assert isinstance(ws.websocket, AsyncMock)


@pytest.mark.asyncio
async def test_websocket_send():
    mock_websocket = AsyncMock()
    ws = WebSocket("ws://test.com")
    ws.websocket = mock_websocket
    await ws.send("test message")
    mock_websocket.send.assert_called_once_with("test message")


@pytest.mark.asyncio
async def test_websocket_receive():
    mock_websocket = AsyncMock()
    mock_websocket.recv.return_value = "test message"
    ws = WebSocket("ws://test.com")
    ws.websocket = mock_websocket
    await ws.receive()
    mock_websocket.recv.assert_called_once()


@pytest.mark.asyncio
async def test_websocket_close():
    mock_websocket = AsyncMock()
    ws = WebSocket("ws://test.com")
    ws.websocket = mock_websocket
    await ws.close()
    mock_websocket.close.assert_called_once()
