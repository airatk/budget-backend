from typing import Any

from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import insert, text

from core.databases.models.utilities.base import BaseModel

from .settings import test_settings
from .utilities.callables import get_records_data_from_json
from .utilities.constants import DATABASE_MAPPING


_POSTGRES_DEFAULT_DATABASE_URL: str = PostgresDsn.build(
    scheme=test_settings.POSTGRES_DRIVER,
    user=test_settings.POSTGRES_USERNAME,
    password=test_settings.POSTGRES_PASSWORD,
    host=test_settings.POSTGRES_HOST,
    port=test_settings.POSTGRES_PORT,
    path='/postgres',
)


test_postgres_engine: AsyncEngine = create_async_engine(
    url=test_settings.POSTGRES_URL,
    poolclass=NullPool,
)


TestPostgresSession: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=test_postgres_engine,
    expire_on_commit=False,
)


async def create_database() -> None:
    engine: AsyncEngine = create_async_engine(
        url=_POSTGRES_DEFAULT_DATABASE_URL,
        isolation_level='AUTOCOMMIT',
    )

    async with engine.connect() as database_connection:
        await database_connection.execute(
            text('CREATE DATABASE "{database_name}"'.format(
                database_name=test_settings.POSTGRES_DATABASE,
            )),
        )

    await engine.dispose()


async def drop_database() -> None:
    engine: AsyncEngine = create_async_engine(
        url=_POSTGRES_DEFAULT_DATABASE_URL,
        isolation_level='AUTOCOMMIT',
    )

    async with engine.connect() as database_connection:
        await database_connection.execute(
            text('DROP DATABASE IF EXISTS "{database_name}" WITH (FORCE)'.format(
                database_name=test_settings.POSTGRES_DATABASE,
            )),
        )

    await engine.dispose()


async def create_database_tables() -> None:
    engine: AsyncEngine = create_async_engine(
        url=test_settings.POSTGRES_URL,
    )

    async with engine.begin() as database_connection:
        await database_connection.run_sync(BaseModel.metadata.create_all)

        for database_mapping_item in DATABASE_MAPPING:
            record_data_list: list[dict[str, Any]] = get_records_data_from_json(
                file_name=database_mapping_item.file_name,
            )

            await database_connection.execute(
                insert(database_mapping_item.model).values(record_data_list),
            )
            await database_connection.execute(
                text('ALTER SEQUENCE {sequence_id} RESTART WITH {sequence_next_value}'.format(
                    sequence_id=database_mapping_item.sequence_id,
                    sequence_next_value=len(record_data_list) + 1,
                )),
            )

    await engine.dispose()
