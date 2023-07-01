from asyncio import BaseTransport, ensure_future
from unittest.mock import Mock

import pytest
from httptools import HttpRequestParser

from core import Application, HttpProtocol, Request


@pytest.mark.asyncio
async def test_http_protocol():
    mock_app = Mock(Application)
    mock_transport = Mock(BaseTransport)
    mock_request_parser = Mock(HttpRequestParser)
    mock_request = Mock(Request, parser=mock_request_parser)

    http_protocol = HttpProtocol(mock_app)

    http_protocol.connection_made(mock_transport)
    assert http_protocol.transport == mock_transport

    http_protocol.data_received(b"GET / HTTP/1.1\r\nHost: localhost:8000\r\n\r\n")
    mock_request_parser.feed_data.assert_called_with(
        b"GET / HTTP/1.1\r\nHost: localhost:8000\r\n\r\n"
    )

    await ensure_future(http_protocol.handle_request(mock_request))
    mock_transport.write.assert_called()
    mock_transport.close.assert_called()
