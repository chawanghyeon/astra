# type: ignore
import asyncio

import uvloop

from core.application import Application
from settings import SERVER_HOST, SERVER_PORT


async def main() -> None:
    app = Application()
    try:
        await app.server.run(SERVER_HOST, SERVER_PORT)
    except KeyboardInterrupt:
        await app.server.stop()
    finally:
        return


if __name__ == "__main__":
    with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
        runner.run(main())
