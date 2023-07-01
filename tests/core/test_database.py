from unittest.mock import Mock, patch

import pytest

from core import Database
from settings import DATABASES


@pytest.mark.asyncio
async def test_database():
    with patch("your_module.asyncpg.create_pool") as mock_create_pool, patch(
        "your_module.AsyncIOMotorClient"
    ) as mock_motor_client, patch("your_module.aiosqlite.connect") as mock_sqlite_connect:
        mock_postgres_pool = Mock()
        mock_create_pool.return_value = mock_postgres_pool

        mock_mongo_client = Mock()
        mock_motor_client.return_value = mock_mongo_client

        mock_sqlite_connection = Mock()
        mock_sqlite_connect.return_value = mock_sqlite_connection

        db = Database()

        # Test PostgreSQL connection
        # DEFAULT_DATABASE = "POSTGRES"
        await db.connect()
        assert db.connection == mock_postgres_pool
        mock_create_pool.assert_called_with(**DATABASES["POSTGRES"])

        await db.disconnect()
        mock_postgres_pool.close.assert_called_once()

        # Test MongoDB connection
        # DEFAULT_DATABASE = "MONGODB"
        await db.connect()
        assert db.connection == mock_mongo_client
        mock_motor_client.assert_called_with(
            f"mongodb://{DATABASES['MONGODB']['host']}:{DATABASES['MONGODB']['port']}"
        )

        db.disconnect()
        mock_mongo_client.close.assert_called_once()

        # Test SQLite connection
        # DEFAULT_DATABASE = "SQLITE"
        await db.connect()
        assert db.connection == mock_sqlite_connection
        mock_sqlite_connect.assert_called_with(DATABASES["SQLITE"]["database"])

        await db.disconnect()
        mock_sqlite_connection.close.assert_called_once()
