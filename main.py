from core.application import Application
from asyncio import run
from settings import SERVER_HOST, SERVER_PORT

if __name__ == "__main__":
    app = Application()
    run(app.run(SERVER_HOST, SERVER_PORT))
