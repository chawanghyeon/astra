from core.application import Application
from asyncio import run

if __name__ == "__main__":
    app = Application()
    run(app.run("127.0.0.1", 8080))
