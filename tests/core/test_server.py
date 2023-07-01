import asyncio
from unittest import mock

import pytest

from core import Application, Server


@pytest.mark.asyncio
async def test_server_run_stop():
    # Mocking the loop and server for testing
    loop = mock.MagicMock()
    server = mock.MagicMock()

    # Replace with the actual Application instance
    app = Application()

    with mock.patch("asyncio.get_event_loop", return_value=loop), mock.patch.object(
        loop, "create_server", return_value=server
    ):
        # create a Server instance
        server_instance = Server(app)

        # Simulate the run method in a separate task because it is blocking
        run_server_task = asyncio.create_task(server_instance.run("localhost", 8000))

        # Wait for the server to start running
        await asyncio.sleep(0.1)

        # Assert that the server is running
        assert server_instance.is_running()

        # Stop the server
        await server_instance.stop()

        # Assert that the server is not running
        assert not server_instance.is_running()

        # Clean up the run server task
        run_server_task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await run_server_task
