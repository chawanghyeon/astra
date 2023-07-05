import asyncio

import pytest

from core.application import Application


@pytest.mark.asyncio
async def test_server_run_stop() -> None:
    loop = asyncio.get_event_loop()
    app = Application()
    server_instance = app.server

    run_server_task = loop.create_task(server_instance.run("localhost", 8000))

    try:
        await asyncio.sleep(1)

        assert server_instance.is_running()

        await server_instance.stop()

        assert server_instance.is_running() is False
    finally:
        run_server_task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await run_server_task
            await loop.shutdown_default_executor()
            await loop.shutdown_asyncgens()
            loop.stop()
            loop.close()
