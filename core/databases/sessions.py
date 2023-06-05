from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.settings import settings


postgres_engine: AsyncEngine = create_async_engine(url=settings.POSTGRES_URL)

PostgresSession: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=postgres_engine,
    expire_on_commit=False,
    autocommit=False,
)
