import pytest
from unittest.mock import AsyncMock
from core.websocket_protocol import WebSocketProtocol


class MockApp:
    class MockRouter:
        dispatch_websocket = AsyncMock()

    router = MockRouter()


@pytest.mark.asyncio
async def test_process_message():
    protocol = WebSocketProtocol(MockApp(), None, None)
    await protocol.process_message("/test", "test message")
    MockApp.router.dispatch_websocket.assert_called_once_with("/test", "test message")
