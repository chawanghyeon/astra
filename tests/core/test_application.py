from unittest.mock import patch

import pytest

from core.application import Application
from core.request import Request
from core.response import Response
from core.status import INTERNAL_SERVER_ERROR
from middlewares.base import BaseMiddleware


class MockMiddleware(BaseMiddleware):
    async def process_request(self, request):
        return request, None

    async def process_response(self, request, response):
        return response


class TestApplication:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.app = Application()
        self.app.middlewares = [MockMiddleware()]

    @pytest.mark.asyncio
    async def test_process_request(self):
        request = Request()
        processed_request, response = await self.app.process_request(request)

        assert processed_request == request
        assert response is None

    @pytest.mark.asyncio
    async def test_process_response(self):
        request = Request()
        response = Response()
        processed_response = await self.app.process_response(request, response)

        assert processed_response == response

    @pytest.mark.asyncio
    async def test_handle_exception(self):
        exception = Exception("Test exception")
        response = await self.app.handle_exception(exception, "Test error")

        assert response.status_code == INTERNAL_SERVER_ERROR

    @pytest.mark.asyncio
    async def test_handle_request(self):
        request = Request()
        with patch.object(self.app.router, "dispatch", return_value=Response()) as mock_dispatch:
            response = await self.app.handle_request(request)

            assert response is not None
            mock_dispatch.assert_called_once_with(request)

    @pytest.mark.asyncio
    async def test_handle_request_with_exception(self):
        request = Request()
        with patch.object(
            self.app.router, "dispatch", side_effect=Exception("Test exception")
        ) as mock_dispatch:
            response = await self.app.handle_request(request)

            assert response.status_code == INTERNAL_SERVER_ERROR
            mock_dispatch.assert_called_once_with(request)
