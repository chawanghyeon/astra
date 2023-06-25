# type: ignore

from asyncio import run

from core.application import Application
from settings import SERVER_HOST, SERVER_PORT


async def main() -> None:
    app = Application()
    try:
        await app.server.run(SERVER_HOST, SERVER_PORT)
    except KeyboardInterrupt:
        await app.server.stop()


if __name__ == "__main__":
    run(main())
