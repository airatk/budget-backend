from typing import AsyncIterator

from fastapi import Depends, Header
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.sessions import define_postgres_session
from core.databases.models import User

from .databases import TestPostgresSession


async def define_test_postgres_session() -> AsyncIterator[AsyncSession]:
    async with TestPostgresSession() as test_postgres_session:
        yield test_postgres_session


async def identify_test_user(
    session: AsyncSession = Depends(define_postgres_session),
    test_username: str = Header(default='test-user'),
) -> User:
    query_result: Result[tuple[User]] = await session.execute(
        select(User).where(User.username == test_username),
    )

    return query_result.unique().scalars().one()
