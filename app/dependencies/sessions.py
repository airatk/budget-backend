from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from core.databases.sessions import PostgresSession


async def define_postgres_session() -> AsyncIterator[AsyncSession]:
    async with PostgresSession() as postgres_session:
        yield postgres_session
