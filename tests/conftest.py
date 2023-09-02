from calendar import monthrange
from datetime import date, datetime
from typing import AsyncIterator

from httpx import AsyncClient
from pytest import fixture

from app import api
from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user

from .mock.databases import (
    create_database,
    create_database_tables,
    drop_database,
)
from .mock.dependencies import define_test_postgres_session, identify_test_user


@fixture(scope='session', autouse=True)
async def manage_database() -> AsyncIterator[None]:
    await drop_database()
    await create_database()
    await create_database_tables()

    yield

    await drop_database()


@fixture(scope='session')
def anyio_backend() -> str:
    return 'asyncio'


@fixture(scope='session')
async def test_client() -> AsyncIterator[AsyncClient]:
    api.dependency_overrides[define_postgres_session] = define_test_postgres_session
    api.dependency_overrides[identify_user] = identify_test_user

    async with AsyncClient(app=api, base_url='http://testserver') as api_test_client:
        yield api_test_client


@fixture(scope='session')
def current_month_days_number() -> int:
    today_date: date = datetime.today().date()

    return monthrange(year=today_date.year, month=today_date.month)[1]
