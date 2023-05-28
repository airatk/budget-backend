from calendar import monthrange
from datetime import date, datetime
from typing import Generator

from fastapi.testclient import TestClient
from pytest import fixture

from app import api
from app.dependencies.sessions import define_postgres_session
from app.dependencies.user import identify_user
from core.databases.models.utilities.base import BaseModel

from .mock.databases import fill_up_test_database, test_postgres_engine
from .mock.dependencies import define_test_postgres_session, identify_test_user


@fixture(scope='module', autouse=True)
def manage_test_database() -> Generator[None, None, None]:
    BaseModel.metadata.create_all(bind=test_postgres_engine)
    fill_up_test_database()

    yield

    BaseModel.metadata.drop_all(bind=test_postgres_engine)


@fixture(scope='session')
def test_client() -> Generator[TestClient, None, None]:
    api.dependency_overrides[define_postgres_session] = define_test_postgres_session
    api.dependency_overrides[identify_user] = identify_test_user

    with TestClient(app=api) as api_test_client:
        yield api_test_client


@fixture
def current_month_days_number() -> int:
    today_date: date = datetime.today().date()

    return monthrange(year=today_date.year, month=today_date.month)[1]
