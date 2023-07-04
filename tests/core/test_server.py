import asyncio
from unittest import mock

import pytest

from core.application import Application


@pytest.mark.asyncio
async def test_server_run_stop() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = Application()

    server_instance = app.server

    with mock.patch.object(server_instance, "run", return_value=None) as mock_run:
        with mock.patch.object(server_instance, "stop", return_value=None) as mock_stop:
            loop.run_until_complete(server_instance.run("localhost", 8000))

            assert server_instance.is_running()

            loop.run_until_complete(server_instance.stop())

            assert not server_instance.is_running()

            mock_run.assert_called_once_with("localhost", 8000)
            mock_stop.assert_called_once()

    loop.close()
