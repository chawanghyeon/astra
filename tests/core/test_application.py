from unittest.mock import Mock, patch

import pytest

from core import Application, Request, Response, Status
from middlewares import BaseMiddleware


# Mock Router and Database as we are not testing them here
@patch("your_module.Router", autospec=True)
@patch("your_module.Database", autospec=True)
@patch("your_module.Server", autospec=True)
@pytest.mark.asyncio
async def test_application(mock_server, mock_database, mock_router):
    with patch("your_module.glob.glob") as mock_glob, patch(
        "your_module.importlib.import_module"
    ) as mock_import_module, patch("your_module.logging") as mock_logging:
        mock_middleware = Mock(spec=BaseMiddleware)

        class MockModule:
            def __init__(self):
                self.MockMiddleware = Mock(return_value=mock_middleware)

        mock_module = MockModule()

        # Mocking the middlewares
        mock_glob.return_value = ["middlewares/mock_middleware.py"]
        mock_import_module.return_value = mock_module

        # Mocking request and response
        mock_request = Mock(spec=Request)
        mock_response = Mock(spec=Response)

        app = Application()

        # Testing _load_views and _load_middlewares
        app._load_views()
        mock_glob.assert_called_once_with("views/*.py")

        app._load_middlewares()
        mock_import_module.assert_called_with("mock_middleware")
        assert app.middlewares == [mock_middleware]

        # Testing handle_request
        mock_router.dispatch.return_value = mock_response
        response = await app.handle_request(mock_request)
        assert response == mock_response

        # Testing handle_exception
        exception = Exception("Test exception")
        error_response = await app.handle_exception(exception, "Test message")
        mock_logging.error.assert_called_once_with("Test message Test exception")
        assert error_response.status_code == Status.INTERNAL_SERVER_ERROR
