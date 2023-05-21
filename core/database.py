import asyncpg
import aiosqlite
from motor.motor_asyncio import AsyncIOMotorClient
from settings import DATABASES, DEFAULT_DATABASE


class Database:
    def __init__(self):
        self.connection = None
        self.database_configs = {
            "POSTGRES": {
                "connect": self._connect_postgres,
                "disconnect": self._disconnect_postgres,
            },
            "MONGODB": {"connect": self._connect_mongodb, "disconnect": self._disconnect_mongodb},
            "SQLITE": {"connect": self._connect_sqlite, "disconnect": self._disconnect_sqlite},
        }

    async def connect(self):
        db_config = self.database_configs.get(DEFAULT_DATABASE)
        if not db_config:
            raise ValueError(f"Unsupported database: {DEFAULT_DATABASE}")
        await db_config["connect"]()

    async def disconnect(self):
        db_config = self.database_configs.get(DEFAULT_DATABASE)
        if not db_config:
            raise ValueError(f"Unsupported database: {DEFAULT_DATABASE}")
        await db_config["disconnect"]()

    async def _connect_postgres(self):
        self.connection = await asyncpg.create_pool(
            host=DATABASES["POSTGRES"]["host"],
            database=DATABASES["POSTGRES"]["database"],
            user=DATABASES["POSTGRES"]["user"],
            password=DATABASES["POSTGRES"]["password"],
        )

    async def _connect_mongodb(self):
        self.connection = AsyncIOMotorClient(
            f"mongodb://{DATABASES['MONGODB']['host']}:{DATABASES['MONGODB']['port']}"
        )

    async def _connect_sqlite(self):
        self.connection = await aiosqlite.connect(DATABASES["SQLITE"]["database"])

    async def _disconnect_postgres(self):
        await self.connection.close()

    async def _disconnect_mongodb(self):
        self.connection.close()

    async def _disconnect_sqlite(self):
        await self.connection.close()